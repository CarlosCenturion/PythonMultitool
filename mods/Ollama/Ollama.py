import requests

def ejecutar_remoto(prompt):
    url = "http://localhost:1234/v1"  # URL del servidor local de Ollama
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

def ejecutar():
    prompt = "Hola, ¿cómo estás?"
    respuesta = ejecutar_remoto(prompt)
    print(f"Respuesta del servidor: {respuesta}")

if __name__ == "__main__":
    ejecutar()
    
