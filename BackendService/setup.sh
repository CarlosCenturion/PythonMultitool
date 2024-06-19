#!/bin/bash

# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
