#  Proyecto M7 — API de Análisis de Sentimientos (TF-IDF + Regresión Logística)

---

##  Descripción General

Este proyecto implementa una **API REST** desarrollada con **FastAPI**, capaz de analizar el **sentimiento (positivo o negativo)** de reseñas o textos en inglés.

El modelo se entrena mediante un **pipeline reproducible** que incluye:

- Limpieza y preprocesamiento de texto.  
- Vectorización **TF-IDF**.  
- Clasificación con **Regresión Logística** (`class_weight="balanced"`).  
- Exportación de artefactos (`.pkl`, `.joblib`, `.json`) listos para despliegue.  

---

##  Estructura del Proyecto

| Carpeta / Archivo | Descripción |
|--------------------|-------------|
| **api/** | Código fuente de la API (FastAPI): incluye `main.py` y los endpoints `/predict` y `/health`. |
| **src/** | Pipeline de preprocesamiento y entrenamiento del modelo. |
| **models/** | Artefactos entrenados (modelo, vectorizador y esquemas JSON). |
| **docs/** | Documentación técnica, métricas y evidencias (`metrics.md`, `model_card.md`). |
| **data/** | Dataset usado para entrenamiento y validación. |
| **Dockerfile** | Configuración para construir la imagen Docker. |
| **requirements.txt** | Dependencias necesarias para ejecutar la API y el modelo. |

---

##  Ejecución Local (sin Docker)

Pasos **completos y secuenciales** para ejecutar la API en tu entorno local.

### 1. Clonar el repositorio


git clone https://github.com/alfonso-morenof/Proyecto_M7.git
cd Proyecto_M7

### 2. Activar entorno de Python   

- Con Anaconda:   
    conda activate m7s27   

- O con entorno virtual estándar:  
    python -m venv env  
    source env/bin/activate   
    env\Scripts\activate   

### 3. Instalar dependencias

  pip install -r requirements.txt    

### 4. Levantar la API localmente

  uvicorn api.main:app --reload   

  Una vez ejecutada, abre tu navegador y accede a:   
  http://127.0.0.1:8000/docs   

Allí encontrarás la documentación interactiva Swagger para probar los endpoints disponibles.

Endpoints principales

| Método   | Endpoint   | Descripción                                                                            |
| -------- | ---------- | -------------------------------------------------------------------------------------- |
| **GET**  | `/health`  | Verifica el estado de la API. Retorna “API funcionando correctamente”.                 |
| **POST** | `/predict` | Recibe un texto en inglés y retorna el sentimiento estimado (`positive` o `negative`). |


Ejemplos de uso:

- Entrada JSON:

{
  "text": "The printer works perfectly and the colors are amazing!"
}


- Salida JSON:

{
  "sentiment": "positive"
}


### Ejecución con Docker (opcional)

Si prefieres ejecutar todo en un contenedor Docker:

1. Construir la imagen   
    docker build -t proyecto_m7_api .

2. Ejecutar el contenedor
    docker run --rm -p 8000:8000 proyecto_m7_api   

3. Probar la API   
    Abre en tu navegador:   
    http://127.0.0.1:8000/docs   

    Desde allí puedes probar el endpoint /predict directamente.


## Métricas y evaluación del modelo

Las métricas de desempeño se encuentran documentadas en:   
    docs/metrics.md   


Incluyen:

- Matriz de confusión.   
- Reporte de clasificación (precision, recall, F1-score).   
- Curva ROC y PR.   
- Evidencias visuales generadas durante la validación.

📂 Artefactos Exportados

La carpeta /models/ contiene los archivos necesarios para ejecutar la API:   

| Archivo                 | Descripción                                            |
| ----------------------- | ------------------------------------------------------ |
| `model_base.joblib`     | Modelo entrenado (Regresión Logística).                |
| `vectorizer_base.pkl`   | Vectorizador TF-IDF ajustado.                          |
| `feature_schema.json`   | Esquema de variables y configuración del vectorizador. |
| `inference_schema.json` | Esquema de entrada/salida para la API de predicción.   |


## Instrucciones para Revisores   

Cualquier persona puede:   
  - Clonar el repositorio.
  - Instalar dependencias.   
  - Ejecutar la API local o vía Docker.   
  - Probar los endpoints desde /docs.

--> No se requiere conexión a base de datos ni configuración adicional. Todo está pre-empaquetado en /models y listo para usar.

## Instrucciones para evaluadores (Docker o Local)

### 1. Ejecución local rápida

git clone https://github.com/alfonso-morenof/Proyecto_M7.git
cd Proyecto_M7
pip install -r requirements.txt
uvicorn api.main:app --reload


### 2. Ejecución con Docker

docker build -t proyecto_m7_api .
docker run --rm -p 8000:8000 proyecto_m7_api

Accede al navegador en: http://127.0.0.1:8000/docs

---
Autor:

Alfonso Moreno   
Bootcamp Ciencia de Datos e Inteligencia Artificial — Universidad del Desarrollo   
email:  alfonso.moreno.farias@gmail.com







