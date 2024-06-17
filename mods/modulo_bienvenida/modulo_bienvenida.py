from termcolor import colored

def ejecutar():
    mensaje = "¡Bienvenido a la aplicación modular de Python!"
    autor = "Autor: Carlos Ezequiel Centurion"
    anio = "Año: 2024"

    print(colored(mensaje, 'cyan', attrs=['bold']))
    print(colored(autor, 'yellow'))
    print(colored(anio, 'green'))

if __name__ == "__main__":
    ejecutar()
5