import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import time
import os
import smtplib
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def WishOnStartup():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello Charly, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello Charly, Good Afternoon")
    else:
        speak("Hello Charly, Good Evening")

def instructions():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening now...")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"You asked: {statement}\n")
        except Exception as e:
            #speak("Pardon me, please say that again")
            return "None"
        return statement.lower()

# New Feature 1: Check Weather
def get_weather(city):
    api_key = "your_openweather_api_key"  # Add your OpenWeatherMap API key here
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        return f"The temperature in {city} is {temp}°C with {weather_desc}. The humidity level is {humidity}%."
    else:
        return "Sorry, I couldn't find the weather for that location."

# New Feature 2: Send Emails
def send_email(receiver_email, subject, message):
    sender_email = "your_email@gmail.com"
    password = "your_password"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_message)
        server.close()
        speak("Email has been sent successfully")
    except Exception as e:
        print(e)
        speak("I couldn't send the email, please try again")

WishOnStartup()

def ejecutar():
     while True:
        #speak("How can I assist you?")
        statement = instructions()

        if 'what is' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("what is", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            speak(results)

        elif 'who is' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("who is", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening YouTube")

        elif 'play' in statement:
            song = statement.replace('play', '')
            speak(f'Playing {song}')
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening Google")

        elif 'send email' in statement:
            speak("Who is the receiver?")
            receiver = instructions()
            speak("What is the subject?")
            subject = instructions()
            speak("What should I say in the email?")
            message = instructions()
            send_email(receiver, subject, message)

        elif 'weather in' in statement:
            city = statement.split("in")[-1].strip()
            weather_info = get_weather(city)
            speak(weather_info)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")

        elif 'open notepad' in statement:
            os.system('notepad')

        elif 'goodbye' in statement or 'bye' in statement or 'shut down' in statement:
            speak("Goodbye!")
            break

        else:
            #speak("Sorry, I don't understand that command.")
            print("No Commands")


if __name__ == '__main__':
    ejecutar()
    
    
   