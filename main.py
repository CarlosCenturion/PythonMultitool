from mainscripts.ui import mostrar_menu_principal, consola_principal, gui_principal
from mainscripts.utils import mostrar_logo

if __name__ == "__main__":
    mostrar_logo()
    eleccion = mostrar_menu_principal()
    if eleccion == "1":
        gui_principal()
    elif eleccion == "2":
        consola_principal()
    else:
        print("Opción no válida. Saliendo...")
