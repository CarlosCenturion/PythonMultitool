from colorama import Fore, Style, init

init(autoreset=True)

notas = []
listas = {}

def crear_nota():
    titulo = input(Fore.CYAN + "Título de la nota: ")
    contenido = input(Fore.CYAN + "Contenido de la nota: ")
    notas.append({"titulo": titulo, "contenido": contenido})
    print(Fore.GREEN + "Nota creada con éxito.")

def ver_notas():
    if notas:
        print(Fore.YELLOW + "Notas registradas:")
        for idx, nota in enumerate(notas, start=1):
            print(Fore.WHITE + f"{idx}. {nota['titulo']} - {nota['contenido']}")
    else:
        print(Fore.RED + "No hay notas registradas.")

def eliminar_nota():
    ver_notas()
    if notas:
        try:
            idx = int(input(Fore.CYAN + "Introduce el número de la nota a eliminar: ")) - 1
            if 0 <= idx < len(notas):
                eliminado = notas.pop(idx)
                print(Fore.GREEN + f"Nota '{eliminado['titulo']}' eliminada con éxito.")
            else:
                print(Fore.RED + "Número de nota no válido.")
        except ValueError:
            print(Fore.RED + "Entrada no válida.")

def crear_lista():
    nombre = input(Fore.CYAN + "Nombre de la lista: ")
    listas[nombre] = []
    print(Fore.GREEN + "Lista creada con éxito.")

def agregar_item():
    nombre_lista = input(Fore.CYAN + "Nombre de la lista: ")
    if nombre_lista in listas:
        item = input(Fore.CYAN + "Item a agregar: ")
        listas[nombre_lista].append({"item": item, "marcado": False})
        print(Fore.GREEN + "Item agregado con éxito.")
    else:
        print(Fore.RED + "Lista no encontrada.")

def marcar_item():
    nombre_lista = input(Fore.CYAN + "Nombre de la lista: ")
    if nombre_lista in listas:
        ver_lista(nombre_lista)
        try:
            idx = int(input(Fore.CYAN + "Introduce el número del item a marcar: ")) - 1
            if 0 <= idx < len(listas[nombre_lista]):
                listas[nombre_lista][idx]["marcado"] = True
                print(Fore.GREEN + "Item marcado con éxito.")
            else:
                print(Fore.RED + "Número de item no válido.")
        except ValueError:
            print(Fore.RED + "Entrada no válida.")
    else:
        print(Fore.RED + "Lista no encontrada.")

def ver_lista(nombre_lista):
    if nombre_lista in listas:
        print(Fore.YELLOW + f"Items en la lista '{nombre_lista}':")
        for idx, item in enumerate(listas[nombre_lista], start=1):
            estado = "X" if item["marcado"] else " "
            print(Fore.WHITE + f"{idx}. [{estado}] {item['item']}")
    else:
        print(Fore.RED + "Lista no encontrada.")

def ver_listas():
    if listas:
        print(Fore.YELLOW + "Listas registradas:")
        for nombre_lista in listas:
            ver_lista(nombre_lista)
    else:
        print(Fore.RED + "No hay listas registradas.")

def ejecutar():
    print(Fore.MAGENTA + "Bienvenido a Notas y Listas")
    while True:
        print(Style.BRIGHT + Fore.BLUE + "\nOpciones:")
        print(Style.BRIGHT + Fore.YELLOW + "1. Crear nota")
        print(Style.BRIGHT + Fore.YELLOW + "2. Ver notas")
        print(Style.BRIGHT + Fore.YELLOW + "3. Eliminar nota")
        print(Style.BRIGHT + Fore.YELLOW + "4. Crear lista de verificación")
        print(Style.BRIGHT + Fore.YELLOW + "5. Agregar item a lista")
        print(Style.BRIGHT + Fore.YELLOW + "6. Marcar item en lista")
        print(Style.BRIGHT + Fore.YELLOW + "7. Ver listas de verificación")
        print(Style.BRIGHT + Fore.YELLOW + "8. Salir")
        opcion = input(Fore.CYAN + "Elige una opción: ")
        if opcion == "1":
            crear_nota()
        elif opcion == "2":
            ver_notas()
        elif opcion == "3":
            eliminar_nota()
        elif opcion == "4":
            crear_lista()
        elif opcion == "5":
            agregar_item()
        elif opcion == "6":
            marcar_item()
        elif opcion == "7":
            ver_listas()
        elif opcion == "8":
            print(Fore.MAGENTA + "Saliendo de Notas y Listas.")
            break
        else:
            print(Fore.RED + "Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    ejecutar()
