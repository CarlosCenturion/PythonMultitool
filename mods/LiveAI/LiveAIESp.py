import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import time
import os
import pyjokes
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[1].id)
# rate = engine.getProperty('rate')
# print (rate)
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def WishOnStartup():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        print("Hola, buenos días")
        speak("Hola, buenos días")
    elif hour >= 12 and hour < 18:
        print("Hola, buenas tardes")
        speak("Hola, buenas tardes")
    else:
        print("Hola, buenas noches")
        speak("Hola, buenas noches")

def instructions():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='es-ES')
            print(f"Has dicho: {statement}\n")

        except Exception as e:
            speak("Disculpa, ¿puedes repetirlo?")
            return "None"
        return statement

def tell_joke():
    joke = pyjokes.get_joke(language='es', category='all')
    print(joke)
    speak(joke)

def get_weather():
    api_key = "TU_API_KEY_DE_OPENWEATHERMAP"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Por favor, menciona el nombre de la ciudad")
    city_name = instructions()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang=es"
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"] - 273.15  # Convertir de Kelvin a Celsius
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        weather_report = f"La temperatura en {city_name} es {current_temperature:.2f} grados Celsius con {weather_description} y una humedad del {current_humidity}%."
        print(weather_report)
        speak(weather_report)
    else:
        speak("Ciudad no encontrada")

def set_reminder(reminders):
    speak("¿Qué quieres que te recuerde?")
    reminder = instructions()
    speak("¿En cuántos minutos quieres que te lo recuerde?")
    minutes = instructions()
    try:
        minutes = int(minutes)
        reminders.append((reminder, time.time() + minutes * 60))
        speak(f"Recordatorio establecido para {reminder} en {minutes} minutos")
    except ValueError:
        speak("No he entendido el tiempo. Por favor, inténtalo de nuevo.")

def check_reminders(reminders):
    current_time = time.time()
    for reminder in reminders[:]:
        if current_time >= reminder[1]:
            speak(f"Recordatorio: {reminder[0]}")
            reminders.remove(reminder)

def open_application(statement):
    if "bloc de notas" in statement:
        os.system("notepad")
        speak("Abriendo el bloc de notas")
    elif "calculadora" in statement:
        os.system("calc")
        speak("Abriendo la calculadora")
    else:
        speak("Aplicación no reconocida")

WishOnStartup()

if __name__ == '__main__':
    reminders = []

    while True:
        check_reminders(reminders)
        speak("¿En qué puedo ayudarte?")
        statement = instructions().lower()
        if statement == 0:
            continue

        if 'qué es' in statement:
            speak('Buscando en Wikipedia...')
            statement = statement.replace("qué es", "")
            results = wikipedia.summary(statement, sentences=3, lang='es')
            speak("Según Wikipedia")
            print(results)
            speak(results)

        elif 'quién es' in statement:
            speak('Buscando en Wikipedia...')
            statement = statement.replace("quién es", "")
            results = wikipedia.summary(statement, sentences=3, lang='es')
            speak("Según Wikipedia")
            print(results)
            speak(results)

        elif 'abrir youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube está abierto")
            time.sleep(5)

        elif 'abrir google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google está abierto")
            time.sleep(5)

        elif 'hora' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"La hora es {strTime}")

        elif 'contar un chiste' in statement:
            tell_joke()

        elif 'clima' in statement:
            get_weather()

        elif 'recordatorio' in statement:
            set_reminder(reminders)

        elif 'abrir' in statement:
            open_application(statement)

        elif 'quién eres' in statement or 'qué puedes hacer' in statement:
            speak('Soy tu asistente personal. Puedo realizar tareas como abrir YouTube, Google Chrome, Gmail y LeetCode, decirte la hora, buscar en Wikipedia, obtener noticias y mucho más.')

        elif "quién te hizo" in statement or "quién te creó" in statement:
            speak("Fui creado por ti.")

        elif "adiós" in statement or "hasta luego" in statement:
            print('Asistente cerrándose. ¡Adiós!')
            speak('Asistente cerrándose. ¡Adiós!')
            break

        time.sleep(2)
