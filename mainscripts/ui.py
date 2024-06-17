from tkinter import *
from mainscripts.modulos import obtener_modulos, ejecutar_modulo, cargar_modulo
from mainscripts.acciones import informacion_modulo, editar_modulo, eliminar_modulo
from mainscripts.utils import mostrar_submenu
from mainscripts.gui_utils import mostrar_submenu_gui
from colorama import Fore

def mostrar_menu_principal():
    print("Selecciona el modo de interfaz:")
    print("1. Interfaz Gráfica de Usuario (GUI)")
    print("2. Interfaz de Consola")
    eleccion = input("Ingresa tu elección: ")
    return eleccion

def consola_principal():
    while True:
        modulos = obtener_modulos()
        mostrar_menu(modulos)
        eleccion = input(f"{Fore.YELLOW}Ingresa tu elección: ")
        try:
            eleccion_numero = int(eleccion)
            if 1 <= eleccion_numero <= len(modulos):
                nombre_modulo = modulos[eleccion_numero - 1]
                submenu(nombre_modulo)
            elif eleccion_numero == len(modulos) + 1:
                print(f"{Fore.CYAN}Saliendo...")
                break
            else:
                print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")
        except ValueError:
            print(f"{Fore.RED}Entrada no válida. Por favor, ingresa un número.")

def mostrar_menu(modulos):
    print(f"{Fore.CYAN}Selecciona un módulo:")
    print(f"")
    for idx, modulo in enumerate(modulos):
        print(f"{Fore.CYAN}{idx + 1}. {modulo.capitalize()}")
    print(f"{Fore.CYAN}{len(modulos) + 1}. Salir")
    print(f"")

def submenu(nombre_modulo):
    while True:
        mostrar_submenu(nombre_modulo)
        eleccion = input(f"{Fore.YELLOW}Ingresa tu elección: ")
        if eleccion == "1":
            modulo = cargar_modulo(nombre_modulo)
            ejecutar_modulo(modulo)
        elif eleccion == "2":
            informacion_modulo(nombre_modulo)
        elif eleccion == "3":
            editar_modulo(nombre_modulo)
        elif eleccion == "4":
            eliminar_modulo(nombre_modulo)
            break
        elif eleccion == "5":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

def gui_principal():
    root = Tk()
    root.title("Gestor de Módulos")

    modulos = obtener_modulos()

    Label(root, text="Selecciona un módulo:", font=("Helvetica", 16)).pack(pady=10)
    for nombre_modulo in modulos:
        Button(root, text=nombre_modulo.capitalize(), command=lambda nm=nombre_modulo: mostrar_submenu_gui(nm)).pack(fill="x")

    root.mainloop()
