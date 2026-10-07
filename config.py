"""Configuración central de ejecución."""
from __future__ import annotations
import os
HOST = os.getenv("ATOMOS_HOST", "127.0.0.1")
PORT = int(os.getenv("ATOMOS_PORT", "5000"))
SECRET_KEY = os.getenv("ATOMOS_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("ATOMOS_DEBUG", "0").lower() in {"1", "true", "yes"}
