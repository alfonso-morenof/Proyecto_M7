import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def limpiar_texto(texto: str) -> str:
    t = (texto or "").lower()
    t = re.sub(r"http\S+|www\S+|https\S+", "", t)   # URLs
    t = re.sub(r"\S*@\S*\s?", "", t)                # emails
    t = re.sub(r"[^a-záéíóúüñ ]", " ", t)           # solo letras y espacios
    t = re.sub(r"\s+", " ", t).strip()              # espacios múltiples
    return t

def aplicar_limpieza(df: pd.DataFrame, col_in: str, col_out: str = "texto_limpio") -> pd.DataFrame:
    df = df.copy()
    df[col_out] = df[col_in].astype(str).apply(limpiar_texto)
    return df

def dividir_datos(df: pd.DataFrame, col_texto: str, col_target: str, test_size: float = 0.20, seed: int = 60):
    X_train, X_val, y_train, y_val = train_test_split(
        df[col_texto], df[col_target],
        test_size=test_size,
        stratify=df[col_target],
        random_state=seed
    )
    return X_train, X_val, y_train, y_val

def construir_vectorizador(ngram_range=(1,2), min_df=2, max_df=0.95,
                           max_features=40000, sublinear_tf=True):
    """Construye un TfidfVectorizer robusto a tipos provenientes de YAML."""
    # --- normalizaciones por si vienen desde config.yml ---
    if isinstance(ngram_range, list):
        ngram_range = tuple(ngram_range)       # YAML -> lista; sklearn exige tupla
    min_df = int(min_df)
    max_df = float(max_df)
    max_features = int(max_features)
    sublinear_tf = bool(sublinear_tf)

    from sklearn.feature_extraction.text import TfidfVectorizer
    return TfidfVectorizer(
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        max_features=max_features,
        sublinear_tf=sublinear_tf
    )


if __name__ == "__main__":
    print("Módulo preproceso cargado correctamente.")
    print("Ejemplo:", limpiar_texto("Check https://site.com EMAIL me@x.com :)  Hola!!!"))

    # === Test de lectura del archivo config.yml ===
import yaml
from pathlib import Path

config_path = Path(__file__).parent / "config.yml"

try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    print("\n✅ Configuración cargada correctamente:")
    print(config)
except Exception as e:
    print("\n❌ Error al leer config.yml:", e)
