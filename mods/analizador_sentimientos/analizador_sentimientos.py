from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import speech_recognition as sr
from colorama import init, Fore, Style
import nltk

# Descargar los datos necesarios de VADER
nltk.download('vader_lexicon')

init(autoreset=True)

def analizar_sentimiento(texto):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(texto)
    return scores['compound']

def traducir_texto(texto, idioma_destino='en'):
    traductor = Translator()
    try:
        traduccion = traductor.translate(texto, dest=idioma_destino)
        return traduccion.text
    except Exception as e:
        print(f"{Fore.RED}Error al traducir el texto: {e}")
        return texto

def detectar_idioma(texto):
    traductor = Translator()
    try:
        deteccion = traductor.detect(texto)
        return deteccion.lang
    except Exception as e:
        print(f"{Fore.RED}Error al detectar el idioma: {e}")
        return None

def reconocimiento_de_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{Fore.YELLOW}Di algo...")
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            print(f"{Fore.CYAN}Texto detectado: {Fore.WHITE}{texto}")
            return texto
        except sr.UnknownValueError:
            print(f"{Fore.RED}No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"{Fore.RED}Error al conectarse con el servicio de reconocimiento de voz; {e}")
        return None

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Análisis de Sentimientos")
        print(f"{Fore.BLUE}1. Ingresar Texto")
        print(f"{Fore.BLUE}2. Usar Reconocimiento de Voz")
        print(f"{Fore.BLUE}3. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            entrada = input(f"{Fore.YELLOW}Texto: ")
        elif eleccion == "2":
            entrada = reconocimiento_de_voz()
            if not entrada:
                continue
        elif eleccion == "3":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")
            continue

        idioma_original = detectar_idioma(entrada)
        if idioma_original and idioma_original != 'en':
            entrada = traducir_texto(entrada, 'en')
            print(f"{Fore.CYAN}Texto traducido: {Fore.WHITE}{entrada}")
        polaridad = analizar_sentimiento(entrada)
        if polaridad > 0:
            sentimiento = f"{Fore.GREEN}Positivo"
        elif polaridad < 0:
            sentimiento = f"{Fore.RED}Negativo"
        else:
            sentimiento = f"{Fore.YELLOW}Neutral"
        print(f"{Fore.CYAN}Sentimiento: {sentimiento} ({polaridad})")

if __name__ == "__main__":
    ejecutar()
