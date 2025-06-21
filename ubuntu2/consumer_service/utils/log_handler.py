import json
from datetime import datetime
import os

def guardar_em_log(fila, dados, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha = f"[{timestamp}] {fila.upper()} → {json.dumps(dados)}\n"

    os.makedirs("logs", exist_ok=True)

    with open(f"logs/{fila}.log", "a") as f:
        f.write(linha)

    print(f"Guardado em logs/{fila}.log")
