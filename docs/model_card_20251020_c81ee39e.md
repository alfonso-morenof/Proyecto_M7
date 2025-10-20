# 🧠 Model Card — Proyecto M7

**Fecha:** 20251020  
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
- Modelo: `model_20251020_c81ee39e.pkl`
- Vectorizador: `vectorizer_20251020_c81ee39e.pkl`
- Feature Schema: `feature_schema_20251020_c81ee39e.json`
- Inference Schema: `inference_schema_20251020_c81ee39e.json`

---

> 📁 Todos los artefactos están almacenados en `/models` y versionados con fecha y hash.