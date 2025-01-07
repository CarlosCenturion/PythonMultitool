import pyttsx3

def listar_voces():
    """
    Lista todas las voces instaladas en el sistema y sus propiedades.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Nombre: {voice.name}")
        print(f"ID: {voice.id}")
        print(f"Idioma: {voice.languages}")
        print("-" * 20)

def leer_texto_en_voz_alta(texto, id_voz=None):
    """
    Esta función convierte el texto proporcionado en voz y lo reproduce con una voz en español.
    """
    engine = pyttsx3.init()

    # Configurar propiedades como la voz, el volumen y la velocidad
    if id_voz:
        engine.setProperty('voice', id_voz)  # Cambia la voz a la ID proporcionada
    engine.setProperty('rate', 150)  # Ajusta la velocidad de la voz
    engine.setProperty('volume', 1)  # Ajusta el volumen al máximo (0.0 a 1.0)

    # Reproducir el texto
    engine.say(texto)

    # Esperar a que termine de hablar
    engine.runAndWait()
    
def ejecutar():
    listar_voces()  # Muestra las voces disponibles en tu sistema

    # Pide al usuario que ingrese texto y selecciona una voz en español
    texto = input("Introduce el texto que deseas escuchar: ")

    # Cambia esto al ID de la voz que prefieras, según lo que arroje listar_voces()
    id_voz_espanol = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech_OneCore\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

    leer_texto_en_voz_alta(texto, id_voz=id_voz_espanol)


if __name__ == "__main__":
    ejecutar()
    