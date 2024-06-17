import importlib
import os
import traceback
from mainscripts.dependencias import instalar_dependencias
from colorama import Fore

def obtener_modulos():
    modulos = []
    ruta_modulos = os.path.join(os.path.dirname(__file__), '../mods')
    for nombre in os.listdir(ruta_modulos):
        ruta_modulo = os.path.join(ruta_modulos, nombre)
        if os.path.isdir(ruta_modulo) and nombre != '__pycache__':
            modulos.append(nombre)
    return modulos

def cargar_modulo(nombre_modulo):
    ruta_modulo = os.path.join('mods', nombre_modulo)
    ruta_reqs = os.path.join(ruta_modulo, 'requirements.txt')
    instalar_dependencias(ruta_reqs, ruta_modulo)

    try:
        print(f"{Fore.YELLOW}Cargando el módulo mods.{nombre_modulo}.{nombre_modulo}...")
        modulo = importlib.import_module(f"mods.{nombre_modulo}.{nombre_modulo}")
        print(f"{Fore.GREEN}Módulo cargado correctamente.")
        print(f"")
        print(f"")
        return modulo
    except ImportError as e:
        print(f"{Fore.RED}Error al cargar el módulo {nombre_modulo}: {e}")
        traceback.print_exc()
        return None

def ejecutar_modulo(modulo):
    if modulo:
        modulo.ejecutar()
