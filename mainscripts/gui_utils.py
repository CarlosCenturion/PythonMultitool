from tkinter import Toplevel, Label, Button
from mainscripts.acciones import informacion_modulo, editar_modulo, eliminar_modulo
from mainscripts.modulos import cargar_modulo, ejecutar_modulo

def ejecutar_modulo_gui(nombre_modulo):
    modulo = cargar_modulo(nombre_modulo)
    if modulo:
        ejecutar_modulo(modulo)

def mostrar_submenu_gui(nombre_modulo):
    submenu = Toplevel()
    submenu.title(f"Opciones para {nombre_modulo.capitalize()}")
    Label(submenu, text=f"Selecciona una opción para {nombre_modulo.capitalize()}:").pack(pady=10)
    Button(submenu, text="Ejecutar Módulo", command=lambda: ejecutar_modulo_gui(nombre_modulo)).pack(fill="x")
    Button(submenu, text="Información del Módulo", command=lambda: informacion_modulo(nombre_modulo)).pack(fill="x")
    Button(submenu, text="Editar Módulo", command=lambda: editar_modulo(nombre_modulo)).pack(fill="x")
    Button(submenu, text="Eliminar Módulo", command=lambda: eliminar_modulo(nombre_modulo)).pack(fill="x")
    Button(submenu, text="Volver al Menú Principal", command=submenu.destroy).pack(fill="x")
