# README.md

# Generador de Tickets desde Informes Técnicos

Este proyecto utiliza FastAPI y GPT para analizar informes técnicos y generar tickets estructurados en formato JSON, incluyendo estatus, acciones necesarias, información relevante y departamento responsable. Además, incluye un anonimizado de datos sensibles para cumplir con regulaciones de privacidad.

---

## 🧾 Estructura del Proyecto
```
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── schemas.py
│   ├── anonymizer.py
│   └── gpt_processor.py
├── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## ⚙️ Requisitos
- Python 3.9+
- Clave de API de OpenAI

## 📦 Instalación
```bash
# Clonar el repositorio
$ git clone https://github.com/tuusuario/proyecto-ticket-ai.git
$ cd proyecto-ticket-ai

# Crear entorno virtual
$ python -m venv venv
$ source venv/bin/activate  # en Windows usar venv\Scripts\activate

# Instalar dependencias
$ pip install -r requirements.txt

# Descargar modelo SpaCy
$ python -m spacy download en_core_web_sm
```

## 🔐 Configuración del entorno
Crea un archivo `.env` en la raíz del proyecto basado en `.env.example`:
```env
OPENAI_API_KEY=sk-tu-clave
```

## 🚀 Ejecución del servidor
```bash
$ uvicorn main:app --reload
```

Abre tu navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para acceder a la interfaz Swagger.

## 📤 Ejemplo de petición
```json
POST /generate_ticket
{
  "caseID": "CASE123456",
  "reportText": "Cliente llama indicando que el dispositivo no carga. Se intenta reinicio. Se programa envío a soporte técnico."
}
```

## ✅ Ejemplo de respuesta
```json
{
  "caseID": "CASE123456",
  "status": "pending",
  "actions": "Enviar el dispositivo a soporte técnico para evaluación de hardware.",
  "info": "Se intentó reinicio sin éxito. Posible fallo del puerto de carga.",
  "department": "soporte_tecnico"
}
```

## 📄 Licencia
MIT

## ✨ Autor
Desarrollado por [Tu Nombre] como prueba técnica para posición de Machine Learning Engineer.
