import json
import os
from tkinter import *
from tkinter import messagebox
from colorama import init, Fore, Style

init(autoreset=True)

PROYECTOS_FILE = os.path.join(os.path.dirname(__file__), 'proyectos.json')

def cargar_proyectos():
    if os.path.exists(PROYECTOS_FILE):
        with open(PROYECTOS_FILE, 'r') as f:
            return json.load(f)
    return []

def guardar_proyectos(proyectos):
    with open(PROYECTOS_FILE, 'w') as f:
        json.dump(proyectos, f, indent=4)

def agregar_proyecto(nombre):
    proyectos = cargar_proyectos()
    proyectos.append({
        'nombre': nombre,
        'tareas': {
            'To Do': [],
            'In Progress': [],
            'Done': []
        }
    })
    guardar_proyectos(proyectos)
    print(f"{Fore.GREEN}Proyecto '{nombre}' agregado con éxito.")

def agregar_tarea(proyecto_idx, columna, tarea):
    proyectos = cargar_proyectos()
    proyecto = proyectos[proyecto_idx]
    proyecto['tareas'][columna].append(tarea)
    guardar_proyectos(proyectos)
    print(f"{Fore.GREEN}Tarea '{tarea}' agregada a '{columna}' en el proyecto '{proyecto['nombre']}'.")

def mover_tarea(proyecto_idx, tarea, from_col, to_col):
    proyectos = cargar_proyectos()
    proyecto = proyectos[proyecto_idx]
    if tarea in proyecto['tareas'][from_col]:
        proyecto['tareas'][from_col].remove(tarea)
        proyecto['tareas'][to_col].append(tarea)
        guardar_proyectos(proyectos)
        print(f"{Fore.GREEN}Tarea '{tarea}' movida de '{from_col}' a '{to_col}' en el proyecto '{proyecto['nombre']}'.")
    else:
        print(f"{Fore.RED}Tarea '{tarea}' no encontrada en '{from_col}'.")

def ver_proyectos():
    proyectos = cargar_proyectos()
    if not proyectos:
        print(f"{Fore.YELLOW}No hay proyectos guardados.")
    else:
        for idx, proyecto in enumerate(proyectos):
            print(f"{Fore.CYAN}{idx + 1}. Proyecto: {Fore.WHITE}{proyecto['nombre']}")
            for columna, tareas in proyecto['tareas'].items():
                print(f"{Fore.CYAN}{columna}:")
                for tarea in tareas:
                    print(f"  {Fore.WHITE}{tarea}")
            print(f"{Fore.MAGENTA}{'-' * 40}")

def seleccionar_proyecto():
    proyectos = cargar_proyectos()
    if not proyectos:
        print(f"{Fore.YELLOW}No hay proyectos guardados.")
        return None
    ver_proyectos()
    while True:
        seleccion = input(f"{Fore.YELLOW}Selecciona un proyecto por su número: ")
        try:
            seleccion_idx = int(seleccion) - 1
            if 0 <= seleccion_idx < len(proyectos):
                return seleccion_idx
            else:
                print(f"{Fore.RED}Número de proyecto no válido. Intenta de nuevo.")
        except ValueError:
            print(f"{Fore.RED}Entrada no válida. Por favor, ingresa un número.")

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Gestor de Proyectos")
        print(f"{Fore.BLUE}1. Agregar Proyecto")
        print(f"{Fore.BLUE}2. Agregar Tarea a Proyecto")
        print(f"{Fore.BLUE}3. Mover Tarea en Proyecto")
        print(f"{Fore.BLUE}4. Ver Proyectos")
        print(f"{Fore.BLUE}5. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            nombre = input("Nombre del proyecto: ")
            agregar_proyecto(nombre)
        elif eleccion == "2":
            proyecto_idx = seleccionar_proyecto()
            if proyecto_idx is not None:
                columna = input("Columna (To Do, In Progress, Done): ")
                tarea = input("Descripción de la tarea: ")
                agregar_tarea(proyecto_idx, columna, tarea)
        elif eleccion == "3":
            proyecto_idx = seleccionar_proyecto()
            if proyecto_idx is not None:
                tarea = input("Descripción de la tarea: ")
                from_col = input("Mover de columna (To Do, In Progress, Done): ")
                to_col = input("Mover a columna (To Do, In Progress, Done): ")
                mover_tarea(proyecto_idx, tarea, from_col, to_col)
        elif eleccion == "4":
            ver_proyectos()
        elif eleccion == "5":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
