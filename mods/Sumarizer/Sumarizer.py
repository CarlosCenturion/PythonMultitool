import os
import requests

def ejecutar2(prompt):
    url = "http://localhost:1234/v1"  # Ajusta la URL si es necesario
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Verifica si hay errores HTTP
        result = response.json()  # Obtiene la respuesta en formato JSON
        return result.get('response', 'No se recibió respuesta del servidor.')
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud: {e}"

def leer_archivo_y_resumir(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            prompt = f"Resume el siguiente texto:\n\n{contenido}"
            return ejecutar2(prompt)
    except FileNotFoundError:
        return "El archivo no fue encontrado."
    except IOError as e:
        return f"Error al leer el archivo: {e}"

def ejecutar():
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'ejemplo.txt')  # Cambia esto a la ruta de tu archivo
    resumen = leer_archivo_y_resumir(ruta_archivo)
    print(f"Resumen del archivo: {resumen}")

if __name__ == "__main__":
    ejecutar()
