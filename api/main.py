# ================================
# FastAPI - API de Sentimiento
# Carga automática de artefactos y endpoints /health, /predict, /predict/batch
# ================================
from __future__ import annotations
import re
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr

from joblib import load
import json

# ------------------------------------------------------
# 0) Paths base (asumo que ejecuto uvicorn desde la raíz)
# ------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"

# ------------------------------------------------------
# 1) Utilidad de limpieza (uso la del módulo si existe)
# ------------------------------------------------------
try:
    # Si tienes la función en src/preproceso.py, la uso para asegurar consistencia
    from src.preproceso import limpiar_texto as _limpiar_texto
    def limpiar_texto(txt: str) -> str:
        return _limpiar_texto(txt or "")
except Exception:
    # Fallback minimal, equivalente al de los notebooks
    def limpiar_texto(txt: str) -> str:
        t = (txt or "").lower()
        t = re.sub(r"http[s]?://\S+|www\.\S+", " ", t)  # URLs
        t = re.sub(r"\S+@\S+\.\S+", " ", t)             # emails
        t = re.sub(r"[^a-záéíóúñü\s]", " ", t)          # solo letras y espacios
        t = re.sub(r"\s+", " ", t).strip()              # espacios múltiples
        return t

# ------------------------------------------------------
# 2) Descubrimiento de artefactos (prioridad: pipeline afinado)
#    - model_tuned.joblib (pipeline completo)
#    - model_base.joblib  (pipeline base)
#    - model_*.pkl  +  vectorizer_*.pkl (se arma pipeline en memoria)
# ------------------------------------------------------
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

def _load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def elegir_artefactos():
    # 1) Preferir pipeline afinado
    tuned = MODELS_DIR / "model_tuned.joblib"
    if tuned.exists():
        return {"type": "pipeline", "path": tuned}

    # 2) Pipeline base
    base = MODELS_DIR / "model_base.joblib"
    if base.exists():
        return {"type": "pipeline", "path": base}

    # 3) Modelo + vectorizador por separado (el más reciente por convención)
    #    Tomo el último alfabéticamente si hubiera varios con timestamp
    modelos = sorted(MODELS_DIR.glob("model_*.pkl"))
    vects   = sorted(MODELS_DIR.glob("vectorizer_*.pkl"))
    if modelos and vects:
        return {"type": "separate", "model": modelos[-1], "vectorizer": vects[-1]}

    # 4) Último recurso: nombres "planos"
    m_plain = MODELS_DIR / "model.pkl"
    v_plain = MODELS_DIR / "vectorizer.pkl"
    if m_plain.exists() and v_plain.exists():
        return {"type": "separate", "model": m_plain, "vectorizer": v_plain}

    raise FileNotFoundError(
        "No encontré artefactos en /models. Esperaba model_tuned.joblib, "
        "o model_base.joblib, o pares model_*.pkl + vectorizer_*.pkl."
    )

ARTEFACTOS = elegir_artefactos()

# ------------------------------------------------------
# 3) Carga del modelo
# ------------------------------------------------------
PIPELINE: Pipeline
MODEL_NAME: str
N_FEATURES: Optional[int] = None
CLASSES: Optional[List[str]] = None
VEC_PARAMS: Optional[Dict[str, Any]] = None

if ARTEFACTOS["type"] == "pipeline":
    PIPELINE = load(ARTEFACTOS["path"])
    MODEL_NAME = ARTEFACTOS["path"].name
    # metadata opcional desde feature_schema_xyz.json si existe
    feature_schema = sorted(MODELS_DIR.glob("feature_schema_*.json"))
    if feature_schema:
        meta = _load_json_if_exists(feature_schema[-1]) or {}
        N_FEATURES = meta.get("n_features")
        VEC_PARAMS = {
            "ngram_range": meta.get("ngram_range"),
            "max_df": meta.get("max_df")
        }
    try:
        CLASSES = list(getattr(PIPELINE[-1], "classes_", []))
    except Exception:
        CLASSES = None

else:
    # Carga por separado y arma pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = load(ARTEFACTOS["vectorizer"])
    model = load(ARTEFACTOS["model"])
    PIPELINE = Pipeline([("tfidf", vectorizer), ("clf", model)])
    MODEL_NAME = f"{ARTEFACTOS['model'].name} + {ARTEFACTOS['vectorizer'].name}"
    try:
        N_FEATURES = getattr(vectorizer, "vocabulary_", None)
        N_FEATURES = len(N_FEATURES) if N_FEATURES else None
        VEC_PARAMS = {
            "ngram_range": getattr(vectorizer, "ngram_range", None),
            "max_df": getattr(vectorizer, "max_df", None)
        }
        CLASSES = list(getattr(model, "classes_", []))
    except Exception:
        pass

# ------------------------------------------------------
# 4) FastAPI app + modelos de request/response
# ------------------------------------------------------
app = FastAPI(
    title="API de Sentimiento — Proyecto M7",
    version="1.0.0",
    description="Servicio REST para inferencia de sentimiento (Logistic Regression + TF-IDF).",
)

MAX_TEXT_LEN = 1000  # seguridad/tiempos

class PredictIn(BaseModel):
    text: constr(min_length=1) = Field(..., description="Texto en lenguaje natural")
    truncate: Optional[int] = Field(
        default=MAX_TEXT_LEN,
        ge=1,
        description="Si el texto excede este tamaño, lo recorto para evitar tiempos altos."
    )

class PredictOut(BaseModel):
    label: str
    proba: Optional[Dict[str, float]] = None
    elapsed_ms: float
    model: str

class BatchIn(BaseModel):
    texts: List[constr(min_length=1)]
    truncate: Optional[int] = Field(default=MAX_TEXT_LEN, ge=1)

class HealthOut(BaseModel):
    status: str
    model: str
    n_features: Optional[int] = None
    classes: Optional[List[str]] = None
    vectorizer: Optional[Dict[str, Any]] = None

# ------------------------------------------------------
# 5) Endpoints
# ------------------------------------------------------
@app.get("/health", response_model=HealthOut)
def health():
    return HealthOut(
        status="ok",
        model=MODEL_NAME,
        n_features=N_FEATURES,
        classes=CLASSES,
        vectorizer=VEC_PARAMS,
    )

def _predict_one(text: str, truncate: int) -> PredictOut:
    if not isinstance(text, str) or not text.strip():
        raise HTTPException(status_code=422, detail="Texto vacío o inválido.")

    raw = text[:truncate] if truncate else text
    t0 = time.time()
    clean = limpiar_texto(raw)
    # predict
    label = str(PIPELINE.predict([clean])[0])
    elapsed = (time.time() - t0) * 1000.0

    # proba si existe
    proba = None
    try:
        probs = PIPELINE.predict_proba([clean])[0]
        proba = {str(CLASSES[i]): float(probs[i]) for i in range(len(probs))}
    except Exception:
        proba = None

    return PredictOut(label=label, proba=proba, elapsed_ms=elapsed, model=MODEL_NAME)

@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    return _predict_one(payload.text, payload.truncate or MAX_TEXT_LEN)

@app.post("/predict/batch", response_model=List[PredictOut])
def predict_batch(payload: BatchIn):
    if len(payload.texts) > 64:
        # límite sano para no saturar en local
        raise HTTPException(status_code=413, detail="Batch demasiado grande (máx 64 textos).")
    return [_predict_one(t, payload.truncate or MAX_TEXT_LEN) for t in payload.texts]
