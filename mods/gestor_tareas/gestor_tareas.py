import json
import os
from colorama import init, Fore, Style

init(autoreset=True)

TAREAS_FILE = os.path.join(os.path.dirname(__file__), 'tareas.json')

def cargar_tareas():
    if os.path.exists(TAREAS_FILE):
        with open(TAREAS_FILE, 'r') as f:
            return json.load(f)
    return []

def guardar_tareas(tareas):
    with open(TAREAS_FILE, 'w') as f:
        json.dump(tareas, f, indent=4)

def agregar_tarea(descripcion):
    tareas = cargar_tareas()
    tareas.append({
        'descripcion': descripcion,
        'completada': False
    })
    guardar_tareas(tareas)
    print(f"{Fore.GREEN}Tarea '{descripcion}' agregada con éxito.")

def eliminar_tarea(descripcion):
    tareas = cargar_tareas()
    tareas = [t for t in tareas if t['descripcion'] != descripcion]
    guardar_tareas(tareas)
    print(f"{Fore.RED}Tarea '{descripcion}' eliminada con éxito.")

def ver_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print(f"{Fore.YELLOW}No hay tareas guardadas.")
    else:
        for tarea in tareas:
            estado = f"{Fore.GREEN}Completada" if tarea['completada'] else f"{Fore.RED}Pendiente"
            print(f"{Fore.CYAN}Descripción: {Fore.WHITE}{tarea['descripcion']} - Estado: {estado}")
            print(f"{Fore.MAGENTA}{'-' * 40}")

def marcar_completada(descripcion):
    tareas = cargar_tareas()
    for tarea in tareas:
        if tarea['descripcion'] == descripcion:
            tarea['completada'] = True
            guardar_tareas(tareas)
            print(f"{Fore.GREEN}Tarea '{descripcion}' marcada como completada.")
            return
    print(f"{Fore.RED}Tarea '{descripcion}' no encontrada.")

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Gestor de Tareas")
        print(f"{Fore.BLUE}1. Agregar Tarea")
        print(f"{Fore.BLUE}2. Eliminar Tarea")
        print(f"{Fore.BLUE}3. Ver Tareas")
        print(f"{Fore.BLUE}4. Marcar Tarea como Completada")
        print(f"{Fore.BLUE}5. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            descripcion = input("Descripción de la tarea: ")
            agregar_tarea(descripcion)
        elif eleccion == "2":
            descripcion = input("Descripción de la tarea a eliminar: ")
            eliminar_tarea(descripcion)
        elif eleccion == "3":
            ver_tareas()
        elif eleccion == "4":
            descripcion = input("Descripción de la tarea a marcar como completada: ")
            marcar_completada(descripcion)
        elif eleccion == "5":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
