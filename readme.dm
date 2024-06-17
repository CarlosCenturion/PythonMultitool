# Gestor de Módulos

Este es un gestor de módulos en Python. Puedes seleccionar y ejecutar diferentes módulos desde un menú principal.

## Estructura del Proyecto

- `main.py`: Archivo principal que gestiona los módulos.
- `mods/`: Directorio que contiene los módulos.
  - `modulo1/`: Directorio del módulo 1.
    - `modulo1.py`: Módulo de ejemplo 1.
  - `modulo2/`: Directorio del módulo 2.
    - `modulo2.py`: Módulo de ejemplo 2.
- `tests/`: Directorio que contiene las pruebas unitarias.
  - `test_modulo1.py`: Pruebas para el módulo 1.
  - `test_modulo2.py`: Pruebas para el módulo 2.
- `requirements.txt`: Archivo que lista las dependencias del proyecto.

## Instrucciones

1. Clonar el repositorio.
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `python main.py`
4. Ejecutar las pruebas: `python -m unittest discover tests`

## Contribuir

1. Hacer un fork del proyecto.
2. Crear una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Hacer commit de los cambios (`git commit -am 'Añadir nueva funcionalidad'`).
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crear un nuevo Pull Request.
