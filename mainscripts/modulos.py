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
        return modulo
    except ImportError as e:
        print(f"{Fore.RED}Error al cargar el módulo {nombre_modulo}: {e}")
        print(f"{Fore.RED}Intentando actualizar requirements.txt y reinstalar dependencias...")
        try:
            with open('requirements.txt', 'a') as req_file:
                req_file.write(f"\n# Dependencias del módulo {nombre_modulo}\n")
                with open(ruta_reqs, 'r') as mod_reqs:
                    req_file.writelines(mod_reqs.readlines())
            instalar_dependencias('requirements.txt', ruta_modulo)
            modulo = importlib.import_module(f"mods.{nombre_modulo}.{nombre_modulo}")
            print(f"{Fore.GREEN}Módulo cargado correctamente tras reinstalar dependencias.")
            return modulo
        except Exception as inner_e:
            print(f"{Fore.RED}Error al cargar el módulo {nombre_modulo} después de reinstalar dependencias: {inner_e}")
            traceback.print_exc()
            return None

def ejecutar_modulo(modulo):
    if modulo:
        try:
            modulo.ejecutar()
        except AttributeError as e:
            print(f"{Fore.RED}Error: el módulo {modulo.__name__} no tiene una función 'ejecutar': {e}")
        except Exception as e:
            print(f"{Fore.RED}Error al ejecutar el módulo {modulo.__name__}: {e}")

if __name__ == "__main__":
    modulos = obtener_modulos()
    for nombre_modulo in modulos:
        modulo = cargar_modulo(nombre_modulo)
        ejecutar_modulo(modulo)
