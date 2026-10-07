"""Punto de entrada de Átomos Perdidos.

Arranca Flask en un proceso separado, espera a que esté disponible y abre
automáticamente una pestaña del navegador.

Uso:
    python start.py
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

from config import HOST, PORT

URL = f"http://{HOST}:{PORT}/"
PID_FILE = Path(__file__).with_name(".atomos_perdidos.pid")


def _server_available() -> bool:
    """Comprueba si el servidor ya está escuchando en HOST:PORT."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex((HOST, PORT)) == 0


def _read_pid() -> int | None:
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError, OSError):
        return None


def _write_pid(pid: int) -> None:
    PID_FILE.write_text(str(pid), encoding="utf-8")


def _remove_pid() -> None:
    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass


def main() -> int:
    if _server_available():
        print(f"Átomos Perdidos ya está ejecutándose en {URL}")
        webbrowser.open_new_tab(URL)
        return 0

    old_pid = _read_pid()
    if old_pid is not None:
        _remove_pid()

    command = [
        sys.executable,
        "-c",
        (
            "from app import app; "
            f"app.run(host={HOST!r}, port={PORT}, debug=False, use_reloader=False)"
        ),
    ]

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    process = subprocess.Popen(
        command,
        cwd=Path(__file__).resolve().parent,
        creationflags=creationflags,
    )
    _write_pid(process.pid)

    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            _remove_pid()
            print("No se pudo iniciar el servidor Flask.")
            return process.returncode or 1

        if _server_available():
            print(f"Átomos Perdidos iniciado: {URL}")
            webbrowser.open_new_tab(URL)
            return 0

        time.sleep(0.2)

    print("El servidor no respondió dentro del tiempo esperado.")
    print(f"Puedes comprobarlo manualmente en {URL}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
