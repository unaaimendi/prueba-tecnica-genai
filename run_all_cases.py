import json
import requests
import subprocess
import time
import os
import signal

# Rutas
CASES_PATH = "data/cases.json"
RESULTS_DIR = "data/results"
API_URL = "http://localhost:8000/ticket"

# Crear carpeta de resultados si no existe
os.makedirs(RESULTS_DIR, exist_ok=True)

# Lanzar servidor FastAPI
server = subprocess.Popen(
    ["uvicorn", "app.main:app", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    preexec_fn=os.setsid
)

try:
    print("Esperando a que el servidor arranque...")
    time.sleep(3)

    with open(CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        case_id = case["caseID"]
        payload = {"caseID": case_id}
        result_path = os.path.join(RESULTS_DIR, f"case_{case_id}.json")

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            content = response.json()

            # Validamos que tiene todos los campos esperados
            required_fields = {"caseID", "status", "actions", "info", "department"}
            if not required_fields.issubset(content.keys()):
                raise ValueError(f"Faltan campos en respuesta: {content}")

            # Guardar solo los campos esperados
            with open(result_path, "w", encoding="utf-8") as f_out:
                json.dump(content, f_out, ensure_ascii=False, indent=2)

            print(f"Caso {case_id} procesado correctamente")

        except Exception as e:
            # Resultado de error
            error_result = {
                "caseID": case_id,
                "status": "error",
                "error": str(e)
            }
            with open(result_path, "w", encoding="utf-8") as f_out:
                json.dump(error_result, f_out, ensure_ascii=False, indent=2)
            print(f"Error en caso {case_id}: {e}")

finally:
    print("Terminando servidor...")
    try:
        os.killpg(os.getpgid(server.pid), signal.SIGTERM)
    except ProcessLookupError:
        print("El servidor ya estaba terminado.")
    print("Todo terminado.")
