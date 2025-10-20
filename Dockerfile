# Imagen base mínima de Python
FROM python:3.12-slim

# Evita archivos .pyc y buffers en stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Paquetes de sistema mínimos (compilación) y limpieza
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# ----- Dependencias Python -----
# Copiamos solo requirements primero para cachear esta capa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----- Código de la app -----
# Copiamos el código fuente y la carpeta api
COPY src/ src/
COPY api/ api/

# Copiamos config donde la lee tu app (ajusta si tu app la espera en otro path)
COPY src/config.yml ./config.yml

# ----- Artefactos del modelo -----
# MUY IMPORTANTE: los modelos NO deben estar en .dockerignore
COPY models/ models/

# Exponer puerto interno de la API
EXPOSE 8000

# Comando de arranque (FastAPI con Uvicorn)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
