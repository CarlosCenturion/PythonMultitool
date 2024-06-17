import os

def generar_estructura(directorio, archivo_salida):
    estructura = []
    with open(archivo_salida, 'w') as f:
        f.write("Estructura del Proyecto\n")
        f.write("=" * 50 + "\n\n")
        for root, dirs, files in os.walk(directorio):
            nivel = root.replace(directorio, '').count(os.sep)
            indentacion = ' ' * 4 * nivel
            f.write(f"{indentacion}{os.path.basename(root)}/\n")
            estructura.append(f"{indentacion}{os.path.basename(root)}/")
            subindentacion = ' ' * 4 * (nivel + 1)
            for file in files:
                if not file.endswith('.pyc') and file != '__pycache__':
                    f.write(f"{subindentacion}{file}\n")
                    estructura.append(f"{subindentacion}{file}")

    return estructura

def imprimir_estructura(estructura):
    print("Estructura del Proyecto")
    print("=" * 50)
    for linea in estructura:
        print(linea)

def ejecutar():
    directorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    archivo_salida = os.path.join(directorio_base, 'estructura_proyecto.txt')
    estructura = generar_estructura(directorio_base, archivo_salida)
    imprimir_estructura(estructura)
    print(f"\nEstructura del proyecto generada en {archivo_salida}")

if __name__ == "__main__":
    ejecutar()
