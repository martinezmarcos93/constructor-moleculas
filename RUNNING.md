# Ejecución de Átomos Perdidos

## Arrancar

    python start.py

El lanzador inicia Flask, espera a que responda y abre una pestaña del navegador.

## Cerrar

    python stop.py

stop.py detiene solamente el proceso cuyo PID fue registrado por start.py.

## Configuración

Variables opcionales:

- ATOMOS_HOST (por defecto 127.0.0.1)
- ATOMOS_PORT (por defecto 5000)
- ATOMOS_DEBUG (por defecto 0)
- ATOMOS_SECRET_KEY (por defecto una clave de desarrollo)

Para desarrollo normal no es necesario configurar ninguna variable.
