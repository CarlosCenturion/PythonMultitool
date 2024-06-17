import json
import os
from colorama import init, Fore, Style

init(autoreset=True)

CONTACTOS_FILE = os.path.join(os.path.dirname(__file__), 'contactos.json')

def cargar_contactos():
    if os.path.exists(CONTACTOS_FILE):
        with open(CONTACTOS_FILE, 'r') as f:
            return json.load(f)
    return []

def guardar_contactos(contactos):
    with open(CONTACTOS_FILE, 'w') as f:
        json.dump(contactos, f, indent=4)

def agregar_contacto(nombre, contacto, nota):
    contactos = cargar_contactos()
    contactos.append({
        'nombre': nombre,
        'contacto': contacto,
        'nota': nota
    })
    guardar_contactos(contactos)
    print(f"{Fore.GREEN}Contacto {nombre} agregado con éxito.")

def eliminar_contacto(nombre):
    contactos = cargar_contactos()
    contactos = [c for c in contactos if c['nombre'] != nombre]
    guardar_contactos(contactos)
    print(f"{Fore.RED}Contacto {nombre} eliminado con éxito.")

def ver_contactos():
    contactos = cargar_contactos()
    if not contactos:
        print(f"{Fore.YELLOW}No hay contactos guardados.")
    else:
        for contacto in contactos:
            print(f"{Fore.CYAN}Nombre: {Fore.WHITE}{contacto['nombre']}")
            print(f"{Fore.CYAN}Contacto: {Fore.WHITE}{contacto['contacto']}")
            print(f"{Fore.CYAN}Nota: {Fore.WHITE}{contacto['nota']}")
            print(f"{Fore.MAGENTA}{'-' * 40}")

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Agenda de Contactos")
        print(f"{Fore.BLUE}1. Agregar Contacto")
        print(f"{Fore.BLUE}2. Eliminar Contacto")
        print(f"{Fore.BLUE}3. Ver Contactos")
        print(f"{Fore.BLUE}4. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            nombre = input("Nombre: ")
            contacto = input("Contacto: ")
            nota = input("Nota: ")
            agregar_contacto(nombre, contacto, nota)
        elif eleccion == "2":
            nombre = input("Nombre del contacto a eliminar: ")
            eliminar_contacto(nombre)
        elif eleccion == "3":
            ver_contactos()
        elif eleccion == "4":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
