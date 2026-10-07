"""Llave de cierre de Átomos Perdidos.

Detiene únicamente el servidor iniciado mediante start.py.

Uso:
    python stop.py
"""

from __future__ import annotations

import os
import signal
import time
from pathlib import Path

PID_FILE = Path(__file__).with_name(".atomos_perdidos.pid")


def _read_pid() -> int | None:
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError, OSError):
        return None


def main() -> int:
    pid = _read_pid()

    if pid is None:
        print("Átomos Perdidos no figura como iniciado por start.py.")
        return 0

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        print("El proceso ya no estaba ejecutándose.")
    except PermissionError:
        print(f"No hay permisos para detener el proceso {pid}.")
        return 1
    else:
        print(f"Servidor detenido (PID {pid}).")

        # Darle un instante para liberar el puerto antes de limpiar el PID.
        time.sleep(0.3)

    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass
    except OSError as exc:
        print(f"Aviso: no se pudo eliminar {PID_FILE.name}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
