from openai import OpenAI
import base64

def ejecutar():
    print("Módulo de Whatsthiss Running")

    # Crear el cliente para la API
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # Pedir al usuario la ruta del archivo
    path = input("Enter a local filepath to an image: ")

    # Leer la imagen y codificarla en base64
    base64_image = ""
    try:
        with open(path.replace("'", ""), "rb") as image_file:
            image = image_file.read()
            base64_image = base64.b64encode(image).decode("utf-8")
    except Exception as e:
        print(f"Couldn't read the image. Make sure the path is correct and the file exists. Error: {e}")
        return

    try:
        # Crear la solicitud de completions
        completion = client.chat.completions.create(
            model="cognitivecomputations/dolphin-2.9-llama3-8b-gguf",
            messages=[
                {
                    "role": "system",
                    "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
            stream=True
        )

        # Procesar y mostrar los resultados
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)

    except Exception as e:
        print(f"Error during API call: {e}")
1
if __name__ == "__main__":
    ejecutar()
