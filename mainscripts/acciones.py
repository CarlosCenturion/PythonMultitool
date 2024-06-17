from colorama import Fore
import os
import traceback

def informacion_modulo(nombre_modulo):
    print(f"{Fore.BLUE}Mostrando información del módulo {nombre_modulo.capitalize()}.")

def editar_modulo(nombre_modulo):
    print(f"{Fore.BLUE}Editando el módulo {nombre_modulo.capitalize()}.")

def eliminar_modulo(nombre_modulo):
    confirmacion = input(f"{Fore.RED}¿Estás seguro de que deseas eliminar el módulo {nombre_modulo.capitalize()}? (s/n): ")
    if confirmacion.lower() == 's':
        ruta_modulo = os.path.join('mods', nombre_modulo)
        try:
            if os.path.isdir(ruta_modulo):
                for root, dirs, files in os.walk(ruta_modulo, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(ruta_modulo)
                print(f"{Fore.GREEN}Módulo {nombre_modulo.capitalize()} eliminado.")
            else:
                print(f"{Fore.RED}No se encontró el módulo {nombre_modulo.capitalize()}.")
        except Exception as e:
            print(f"{Fore.RED}Error al eliminar el módulo {nombre_modulo}: {e}")
            traceback.print_exc()
