FROM python:3.11-slim

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone el puerto si hace falta (por ejemplo para FastAPI)
EXPOSE 8000

# Ejecuta el script principal
CMD ["python", "run_all_cases.py"]
