import datetime
import json
import logging
import os
import sys

# Observabilidad: logs estructurados, no solo "OK"
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}',
)
log = logging.getLogger("hora_sistema")

OUTPUT_FILE = "hora.json"


def leer_hora():
    return datetime.datetime.utcnow().isoformat() + "Z"


def escribir_fichero(hora):
    # Idempotencia: cada ejecución sobrescribe con datos completos,
    # no acumula ni depende del estado anterior
    data = {"ultima_ejecucion": hora, "status": "ok"}
    try:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f)
        log.info(f"Fichero escrito correctamente: {hora}")
    except OSError as e:
        # Manejo de errores no negociable: si falla, se sabe
        log.error(f"Fallo al escribir fichero: {e}")
        sys.exit(1)  # código de salida != 0 → GitHub Actions lo marca como fallo


if __name__ == "__main__":
    hora = leer_hora()
    escribir_fichero(hora)
