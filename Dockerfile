# Imagen base con Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Copiar los archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && python -m spacy link es_core_news_md es_core_news_md

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando por defecto
CMD ["python", "run_all_cases.py"]