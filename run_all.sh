#!/bin/bash

# Activar entorno virtual
source venv/bin/activate

source set_env.sh

# Lanzar FastAPI en segundo plano
echo "🚀 Lanzando el servidor..."
uvicorn app.main:app --reload > server.log 2>&1 &
SERVER_PID=$!

# Esperar hasta que el servidor esté disponible
echo "🕐 Esperando a que el servidor arranque..."
until curl -s http://127.0.0.1:8000/docs > /dev/null; do
  sleep 1
done

# Ejecutar script Python
echo "⚙️ Ejecutando casos..."
python app/run_all_cases.py

# Matar el servidor
echo "🛑 Parando servidor (PID $SERVER_PID)..."
kill $SERVER_PID

echo "✅ Todo terminado."
