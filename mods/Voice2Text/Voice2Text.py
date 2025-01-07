import speech_recognition as sr

def reconocer_voz_desde_microfono():
    """
    Esta función captura audio desde el micrófono y lo convierte en texto.
    Devuelve el texto reconocido o 'None' si no se puede reconocer el audio.
    """
    recognizer = sr.Recognizer()

    # Usar el micrófono como fuente de audio
    with sr.Microphone() as source:
        print("Ajustando el ruido ambiente, por favor espere...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listo para escuchar. Hable ahora...")

        # Captar el audio
        audio = recognizer.listen(source)

        try:
            # Usar Google Web Speech API para reconocer el audio
            print("Reconociendo...")
            texto = recognizer.recognize_google(audio, language='es-ES')  # Cambia el idioma si es necesario
            print(f"Texto reconocido: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            return None
        except sr.RequestError as e:
            print(f"No se pudo completar la solicitud a Google Speech Recognition; {e}")
            return None

def ejecutar():
    """
    Función principal que ejecuta el reconocimiento de voz.
    """
    texto = reconocer_voz_desde_microfono()
    if texto:
        print(f"Texto final: {texto}")
    else:
        print("No se pudo obtener ningún texto.")

if __name__ == "__main__":
    ejecutar()
