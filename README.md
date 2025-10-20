# Proyecto M7 — API de Análisis de Sentimientos (TF-IDF + Logistic Regression)

## 📘 Descripción
Este proyecto implementa una API REST basada en **FastAPI**, capaz de analizar sentimientos en reseñas o textos en inglés.  
El modelo fue entrenado usando un pipeline de preprocesamiento, vectorización **TF-IDF** y clasificación mediante **Regresión Logística (class_weight='balanced')**.

---

## ⚙️ Estructura del Proyecto

api/ → Lógica de la API REST (FastAPI)
data/ → Datasets de entrenamiento y validación
docs/ → Documentación técnica y métricas
models/ → Artefactos entrenados (modelo, vectorizador, esquemas)
src/ → Código fuente de preprocesamiento y configuración
tests/ → Pruebas unitarias e integración

---


## Ejecución Local

### Activar entorno virtual
```bash
conda activate m7s27

---

### Instalar dependencias

```bash
pip install -r requirements.txt

---

### Levantar la API

```bash
uvicorn api.main:app --reload
