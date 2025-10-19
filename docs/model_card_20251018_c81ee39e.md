# 🧠 Model Card — Proyecto M7

**Fecha:** 20251018  
**Hash:** c81ee39e  
**Modelo:** Logistic Regression (TF-IDF + class_weight='balanced')  
**Dataset:** Google Play Store Reviews  
**Autor:** Alfonso Moreno  

---

## ⚙️ Configuración del Modelo
- Vectorizador: TF-IDF (unigramas)
- Max features: 30.000  
- min_df: 3  
- max_df: 0.90  
- Sublinear TF: True  
- Clasificador: Logistic Regression (`liblinear`, C=5, max_iter=1000)

---

## 📊 Métricas principales
| Métrica | Valor |
|----------|--------|
| Accuracy | 0.896 |
| F1-macro | 0.8627 |
| Cross-val (5 folds) | 0.863 ± 0.01 |

---

## 📋 Supuestos y Límites
- El modelo asume texto en español previamente limpiado y tokenizado.
- No se recomienda para textos con emojis, ironía o sarcasmo explícito.
- Entrenado con dataset equilibrado (`class_weight='balanced'`).

---

## 🧩 Archivos Exportados
- Modelo: `model_20251018_c81ee39e.pkl`
- Vectorizador: `vectorizer_20251018_c81ee39e.pkl`
- Feature Schema: `feature_schema_20251018_c81ee39e.json`
- Inference Schema: `inference_schema_20251018_c81ee39e.json`

---

## 🧪 9.2 Pruebas de Inferencia — API REST (FastAPI)

A continuación documento las pruebas realizadas a la API REST desarrollada en el **Bloque 9**, utilizando el modelo optimizado (`model_tuned.joblib`) con FastAPI y Uvicorn.

### 🔹 Endpoints operativos
- **GET `/health`** → Verifica el estado del servicio y muestra información del modelo cargado.  
- **POST `/predict`** → Recibe texto individual y devuelve el sentimiento estimado.  
- **POST `/predict/batch`** → Recibe múltiples textos en una sola solicitud y entrega predicciones por lote.  

El servicio corre correctamente en `http://127.0.0.1:8000`, con documentación automática accesible en `http://127.0.0.1:8000/docs`.

---

### 🔹 Pruebas funcionales

#### ✅ 1. Prueba de endpoint `/health`
**Entrada:**  
URL: `http://127.0.0.1:8000/health`

**Salida esperada:**
```json
{
  "status": "ok",
  "model": "model_tuned.joblib",
  "classes": ["Negative", "Neutral", "Positive"],
  "vectorizer": {"type": "TF-IDF"}
}

## 9.3 Pruebas de Inferencia — API REST (FastAPI)

### Endpoint probado: `/predict/batch`
Se validó el funcionamiento del servicio REST enviando tres textos representativos al endpoint `/predict/batch` desde Swagger UI (`http://127.0.0.1:8000/docs`).

**Entrada JSON:**
```json
{
  "texts": [
    "The new Epson printer works perfectly and I really like its speed.",
    "This model is too slow and keeps jamming.",
    "It’s okay, but could be improved."
  ]
}


---

> 📁 Todos los artefactos están almacenados en `/models` y versionados con fecha y hash.