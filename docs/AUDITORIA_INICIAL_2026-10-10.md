# Auditoría inicial y hoja de ruta — Átomos Perdidos

Fecha: 2026-10-10

## Estado verificado

- La rama principal es `main`; al iniciar esta auditoría no había otras ramas remotas ni PR abiertos.
- El workflow `.github/workflows/tests.yml` ejecuta `pytest -q`, pero el último run registrado en `main` (7 de octubre de 2026) termina en fallo en ese paso. La instalación de dependencias sí finaliza correctamente.
- `tests/test_molecular_structure.py` importaba VSEPR desde el módulo antiguo `vsepr`, pero la arquitectura actual lo ubica en `atomos_perdidos.core.vsepr`.
- `tests/test_missions.py` compara la predicción del reactivo limitante con `H2`/ `O2`, que son las etiquetas reales que devuelve el motor; una prueba previa enviaba `H2` en una situación cuyo reactivo limitante es `O2`.
- El modelo de estructura molecular aceptaba símbolos arbitrarios, aunque el resto de los servicios depende de una tabla periódica cerrada de 118 elementos.

## Correcciones en la rama de trabajo

La rama `fix/test-suite-and-chemistry-guards` corrige el import de VSEPR en la prueba, ajusta la expectativa de la misión de agua y añade validación de símbolos y pruebas negativas.

## Lo que falta, por prioridad

1. **Reparar y ejecutar CI**: inspeccionar los resultados completos de pytest y conseguir una ejecución verde.
2. **Pruebas HTTP de Flask**: comprobar las rutas principales y las APIs de errores, límites de entrada y sesiones. Actualmente las pruebas cubren sobre todo funciones de dominio.
3. **Validación de payloads**: unificar respuestas 400 para JSON mal formado, tipos erróneos, valores fuera de rango y estructuras demasiado grandes; revisar los límites que actualmente sólo se aplican en algunas rutas.
4. **Corrección química**: ampliar pruebas del balanceador con reacciones con varios grados de libertad, fórmulas inválidas, empate estequiométrico y entradas límite. La fórmula química válida no prueba por sí sola que una estructura concreta sea posible.
5. **Polaridad**: sustituir la heurística actual basada en un centro y diferencias de electronegatividad por suma vectorial de dipolos para los casos geométricos soportados, o acotar explícitamente su alcance; probar CO2, H2O, NH3 y geometrías simétricas.
6. **Persistencia**: la sesión predeterminada de Flask es una cookie firmada y tiene capacidad limitada; galería/progreso no equivalen a guardado permanente y el secreto de desarrollo debe configurarse al desplegar.
7. **Accesibilidad y uso móvil**: revisión manual de contraste, navegación por teclado, etiquetas de formulario, tamaño táctil y reducción de movimiento.
8. **Experiencia de juego**: prueba integral de campaña, misiones, constructor, galería y recompensas, incluida continuidad al reiniciar sesión.

## Alcance de esta pasada

Estos cambios no se presentan como una validación química profesional ni como prueba de que el conjunto de tests ya pasa. Hace falta ejecutar CI y revisar los logs de pytest antes de integrar en `main`.
