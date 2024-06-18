import datetime
from colorama import Fore, Style, init

init(autoreset=True)

actividades = []

def registrar_actividad():
    nombre = input(Fore.CYAN + "Nombre de la actividad: ")
    fecha = input(Fore.CYAN + "Fecha de la actividad (YYYY-MM-DD HH:MM): ")
    try:
        fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")
        actividades.append({"nombre": nombre, "fecha": fecha})
        print(Fore.GREEN + "Actividad registrada con éxito.")
    except ValueError:
        print(Fore.RED + "Formato de fecha incorrecto.")

def mostrar_actividades():
    if actividades:
        print(Fore.YELLOW + "Actividades registradas:")
        for idx, actividad in enumerate(actividades, start=1):
            print(Fore.WHITE + f"{idx}. {actividad['nombre']} - {actividad['fecha']}")
    else:
        print(Fore.RED + "No hay actividades registradas.")

def eliminar_actividad():
    mostrar_actividades()
    if actividades:
        try:
            idx = int(input(Fore.CYAN + "Introduce el número de la actividad a eliminar: ")) - 1
            if 0 <= idx < len(actividades):
                eliminado = actividades.pop(idx)
                print(Fore.GREEN + f"Actividad '{eliminado['nombre']}' eliminada con éxito.")
            else:
                print(Fore.RED + "Número de actividad no válido.")
        except ValueError:
            print(Fore.RED + "Entrada no válida.")

def ejecutar():
    print(Fore.MAGENTA + "Bienvenido al Gestor de Tiempo")
    while True:
        print(Style.BRIGHT + Fore.BLUE + "\nOpciones:")
        print(Style.BRIGHT + Fore.YELLOW + "1. Registrar actividad")
        print(Style.BRIGHT + Fore.YELLOW + "2. Mostrar actividades")
        print(Style.BRIGHT + Fore.YELLOW + "3. Eliminar actividad")
        print(Style.BRIGHT + Fore.YELLOW + "4. Salir")
        opcion = input(Fore.CYAN + "Elige una opción: ")
        if opcion == "1":
            registrar_actividad()
        elif opcion == "2":
            mostrar_actividades()
        elif opcion == "3":
            eliminar_actividad()
        elif opcion == "4":
            print(Fore.MAGENTA + "Saliendo del Gestor de Tiempo.")
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    ejecutar()
