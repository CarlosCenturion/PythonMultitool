import os
import pygame
import yt_dlp
import imageio_ffmpeg as ffmpeg

# Inicializamos pygame
pygame.mixer.init()

# Definir la carpeta de descargas dentro de la carpeta donde se ejecuta el script
CARPETA_RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_DESCARGAS = os.path.join(CARPETA_RAIZ, "Descargas", "YTMP3")

# Crear la carpeta si no existe
os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

def descargar_audio(url):
    # Obtener el ID del video de la URL
    video_id = url.split('=')[-1]

    # Ruta de ffmpeg proporcionada por imageio-ffmpeg
    ffmpeg_location = ffmpeg.get_ffmpeg_exe()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(CARPETA_DESCARGAS, f'{video_id}.%(ext)s'),  # Guardar en la carpeta Descargas/YTMP3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_location  # Usar la ruta de ffmpeg descargada por imageio-ffmpeg
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)  # Obtiene el nombre final del archivo

    # Cambiar extensión a .mp3 si es necesario
    audio_file = filename.rsplit('.', 1)[0] + ".mp3"
    
    return audio_file

def reproducir_audio(ruta_audio):
    pygame.mixer.music.load(ruta_audio)
    pygame.mixer.music.play()

def frenar_audio():
    pygame.mixer.music.stop()

# Función original (para uso interactivo)
def ejecutar():
    url = input("Introduce la URL del video de YouTube: ")
    audio_file = descargar_audio(url)
    print(f"Reproduciendo música desde {audio_file}...")
    reproducir_audio(audio_file)

    while True:
        comando = input("Escribe 'frenar' para detener la música: ").lower()
        if comando == 'frenar':
            frenar_audio()
            break

# Función para uso remoto (recibe la URL y devuelve la ruta del archivo .mp3)
def ejecutar_remoto(url):
    audio_file = descargar_audio(url)
    return audio_file

# Código que solo se ejecuta si el script es llamado directamente
if __name__ == "__main__":
    ejecutar()
