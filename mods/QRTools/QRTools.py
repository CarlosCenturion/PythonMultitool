import qrcode
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
from colorama import init, Fore
import os

init(autoreset=True)

def generar_qr(contenido, ruta_salida, version, fill_color, back_color, box_size, border):
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(contenido)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    img.save(ruta_salida)
    print(f"{Fore.GREEN}Código QR generado y guardado en {ruta_salida}")

def leer_qr(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        print(f"{Fore.CYAN}Tipo: {obj.type}")
        print(f"{Fore.CYAN}Datos: {obj.data.decode('utf-8')}")

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Gestor de Códigos QR")
        print(f"{Fore.BLUE}1. Generar Código QR")
        print(f"{Fore.BLUE}2. Leer Código QR")
        print(f"{Fore.BLUE}3. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            contenido = input(f"{Fore.YELLOW}Introduce el contenido del Código QR: ")
            nombre_archivo = input(f"{Fore.YELLOW}Introduce el nombre del archivo para guardar el Código QR (ej. qr_code.png): ")
            ruta_salida = os.path.join('Descargas', 'QRCodes', nombre_archivo)
            
            version = int(input(f"{Fore.YELLOW}Introduce la versión (1-40): "))
            fill_color = input(f"{Fore.YELLOW}Introduce el color de relleno (fill_color, ej. black): ")
            back_color = input(f"{Fore.YELLOW}Introduce el color de fondo (back_color, ej. white): ")
            box_size = int(input(f"{Fore.YELLOW}Introduce el tamaño de cada caja (box_size, ej. 10): "))
            border = int(input(f"{Fore.YELLOW}Introduce el tamaño del borde (border, ej. 4): "))
            
            generar_qr(contenido, ruta_salida, version, fill_color, back_color, box_size, border)
        elif eleccion == "2":
            ruta_imagen = input(f"{Fore.YELLOW}Introduce la ruta de la imagen del Código QR a leer: ")
            if os.path.exists(ruta_imagen):
                leer_qr(ruta_imagen)
            else:
                print(f"{Fore.RED}La ruta de la imagen no existe. Intenta de nuevo.")
        elif eleccion == "3":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
