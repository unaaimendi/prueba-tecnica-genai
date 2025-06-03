# README.md

# 🧾 Ticket Generator API

Este proyecto es una API REST construida con **FastAPI** que utiliza **OpenAI** y **SpaCy** para generar tickets automáticamente a partir de reportes de incidentes. El sistema carga casos preexistentes, anonimiza los datos personales y genera propuestas de resolución estructuradas por departamento.

---

## 🚀 Características

- Generación automática de tickets usando **OpenAI GPT-3.5 Turbo**
- Anonimización de datos sensibles usando **expresiones regulares** y **entidades nombradas**
- Dockerizado para fácil despliegue

---

## 🧾 Estructura del Proyecto
```
.
├── app/
│   ├── main.py             # Punto de entrada de FastAPI
│   ├── schemas.py
│   ├── services.py
│   ├── anonymizer.py
│   ├── utils.py
│   ├── router.py
│
├── data/
│   ├── departments.json
│   ├── cases.json
│   ├── results/
│
├── prompt/
│   └── ticket_prompt.yml
│
├── prueba/
│   └── prueba.docx
│
├── tests/
│   ├── test_anonymizer.py
│   ├── test_services.py
│
├── requirements.txt
├── Dockerfile
├── README.md
├── run_all.sh
├── run.sh
├── set_env.sh
├── run_all_cases.py
├── .gitignore
└── .dockerignore

```

## ⚙️ Requisitos
- Python 3.11
- Clave de API de OpenAI
- Docker 🐳
- Docker Compose

## 📦 Instalación
```bash
# Clonar el repositorio
$ git clone https://github.com/unaaimendi/prueba-tecnica-genai.git
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
Introduce tu clave de Openai en el fichero set_env.sh ubicado en la raiz del proyecto:
```set_env.sh:
OPENAI_API_KEY=sk-tu-clave
```

---

## 🚀 Ejecución del servidor

Ejecución de todos los casos incluidos en cases.json

docker-compose up --build

También se puede ejecutar mediante run_all.sh

## 📤 Ejecución del servidor basica

Ejecutar run.sh mediante:

./run.sh

Abre tu navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para acceder a la interfaz, aqui podras poner el número de caso que quieres probar y comprobar la respuesta.

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

## ✅ Testeo

Existen 2 clases de test para testear la anonimización de la información de los usuarios y del servicio.

## ✨ Autor
Desarrollado por Unai Mendiondo como prueba técnica para posición Capgemini.
