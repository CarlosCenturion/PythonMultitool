import os
import configparser
import subprocess

CONFIG_FILE = 'config.ini'

def leer_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'FFmpeg' in config and 'path' in config['FFmpeg']:
            return config['FFmpeg']['path']
    return None

def guardar_config(ffmpeg_path):
    config = configparser.ConfigParser()
    config['FFmpeg'] = {'path': ffmpeg_path}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def verificar_ffmpeg(ffmpeg_path):
    try:
        for tool in ["ffmpeg", "ffprobe"]:
            tool_path = os.path.join(ffmpeg_path, f"{tool}.exe")
            subprocess.run([tool_path, "-version"], check=True, capture_output=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def obtener_ruta_ffmpeg():
    ffmpeg_path = leer_config()
    if ffmpeg_path and verificar_ffmpeg(ffmpeg_path):
        return ffmpeg_path

    while True:
        ffmpeg_path = input("Ingrese la ruta al directorio que contiene FFmpeg (o 'q' para salir): ")
        if ffmpeg_path.lower() == 'q':
            return None
        if verificar_ffmpeg(ffmpeg_path):
            guardar_config(ffmpeg_path)
            return ffmpeg_path
        print("FFmpeg o ffprobe no encontrados en la ruta especificada. Intente de nuevo.")

def configurar_ffmpeg(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    os.environ["FFMPEG_BINARY"] = os.path.join(ffmpeg_path, "ffmpeg.exe")
    os.environ["FFPROBE_BINARY"] = os.path.join(ffmpeg_path, "ffprobe.exe")

# Obtener y configurar FFmpeg antes de importar pydub
ffmpeg_path = obtener_ruta_ffmpeg()
if ffmpeg_path:
    configurar_ffmpeg(ffmpeg_path)
else:
    print("No se pudo configurar FFmpeg. Saliendo del programa.")
    exit()

# Ahora importamos las otras bibliotecas
import speech_recognition as sr
from pydub import AudioSegment
import io

def transcribir_audio(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return f"Error: El archivo {ruta_archivo} no existe."

    try:
        # Inicializar el reconocedor
        recognizer = sr.Recognizer()

        # Leer el archivo .ogg y convertirlo a formato compatible con speech_recognition
        audio = AudioSegment.from_ogg(ruta_archivo)
        buffer = io.BytesIO()
        audio.export(buffer, format="wav")
        buffer.seek(0)

        # Realizar la transcripción
        with sr.AudioFile(buffer) as source:
            audio_data = recognizer.record(source)

        texto = recognizer.recognize_google(audio_data, language="es-ES")
        return texto
    except sr.UnknownValueError:
        return "No se pudo entender el audio"
    except sr.RequestError as e:
        return f"Error en la solicitud al servicio de reconocimiento de voz: {e}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def guardar_transcripcion(texto, ruta_salida):
    try:
        with open(ruta_salida, "w", encoding="utf-8") as file:
            file.write(texto)
        return True
    except Exception as e:
        print(f"Error al guardar la transcripción: {str(e)}")
        return False

def procesar_archivo(ruta_entrada):
    ruta_salida = os.path.splitext(ruta_entrada)[0] + ".txt"
    texto_transcrito = transcribir_audio(ruta_entrada)
    if guardar_transcripcion(texto_transcrito, ruta_salida):
        print(f"La transcripción se ha guardado en {ruta_salida}")
    else:
        print(f"No se pudo guardar la transcripción para {ruta_entrada}")

def procesar_carpeta(ruta_carpeta):
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(".ogg"):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            procesar_archivo(ruta_completa)

def main():
    while True:
        print("\n1. Transcribir un archivo")
        print("2. Transcribir una carpeta completa")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == "1":
            ruta_entrada = input("Ingrese la ruta del archivo de audio .ogg: ")
            procesar_archivo(ruta_entrada)
        elif opcion == "2":
            ruta_carpeta = input("Ingrese la ruta de la carpeta con archivos .ogg: ")
            procesar_carpeta(ruta_carpeta)
        elif opcion == "3":
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def ejecutar():
    main()

if __name__ == "__main__":
    ejecutar()