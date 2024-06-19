import importlib
import os
import sys
import subprocess
from colorama import init, Fore

init(autoreset=True)

def instalar_dependencias(ruta_reqs):
    if os.path.exists(ruta_reqs):
        print(f"{Fore.YELLOW}Instalando dependencias desde {ruta_reqs}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', ruta_reqs])
            print(f"{Fore.GREEN}Dependencias instaladas correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error al instalar dependencias del módulo: {e}")
    else:
        print(f"{Fore.RED}No se encontró el archivo {ruta_reqs}.")

def obtener_versiones():
    versions_path = os.path.join(os.path.dirname(__file__), 'versions')
    versiones = [f for f in os.listdir(versions_path) if f.startswith('v') and f.endswith('.py')]
    return versiones

def mostrar_menu(versiones):
    print(f"{Fore.CYAN}Selecciona una versión del web scrapper para ejecutar:")
    for idx, version in enumerate(versiones):
        print(f"{Fore.CYAN}{idx + 1}. {version}")
    print(f"{Fore.CYAN}{len(versiones) + 1}. Salir")
    print(f"")

def cargar_y_ejecutar_version(version):
    version_path = os.path.join(os.path.dirname(__file__), 'versions', version)
    try:
        spec = importlib.util.spec_from_file_location(version[:-3], version_path)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[version[:-3]] = modulo
        spec.loader.exec_module(modulo)
        print(f"{Fore.GREEN}Módulo {version} cargado correctamente.")
        modulo.ejecutar()
    except ImportError as e:
        print(f"{Fore.RED}Error al cargar el módulo {version}: {e}")

def ejecutar():
    while True:
        versiones = obtener_versiones()
        mostrar_menu(versiones)
        eleccion = input(f"{Fore.YELLOW}Ingresa tu elección: ")
        try:
            eleccion_numero = int(eleccion)
            if 1 <= eleccion_numero <= len(versiones):
                version_seleccionada = versiones[eleccion_numero - 1]
                cargar_y_ejecutar_version(version_seleccionada)
            elif eleccion_numero == len(versiones) + 1:
                print(f"{Fore.CYAN}Saliendo...")
                break
            else:
                print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")
        except ValueError:
            print(f"{Fore.RED}Entrada no válida. Por favor, ingresa un número.")

if __name__ == "__main__":
    ejecutar()
