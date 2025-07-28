import speech_recognition as sr
import pyttsx3
import requests
import time
from datetime import datetime

# Replace with your actual API keys
WEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY'

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    print(f"💬 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"🗣 You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, the speech service is down.")
        return ""

def get_weather(city):
    if not city:
        speak("You didn't provide a city name.")
        return
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res.get('main'):
            temp = res['main']['temp']
            desc = res['weather'][0]['description']
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
        else:
            speak(f"Could not fetch weather for {city}.")
    except Exception as e:
        speak("There was a problem fetching the weather.")
        print(e)

def get_news():
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'
        res = requests.get(url).json()
        articles = res.get("articles", [])
        if articles:
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles[:3]):
                speak(article['title'])
        else:
            speak("Couldn't find any news.")
    except Exception as e:
        speak("There was an error fetching news.")
        print(e)

# Reminder Functionality
reminders = []

def set_reminder(text, delay_sec):
    remind_time = time.time() + delay_sec
    formatted_time = datetime.fromtimestamp(remind_time).strftime('%H:%M:%S')
    reminders.append((remind_time, text))
    speak(f"Reminder set for '{text}' at {formatted_time}.")

def check_reminders():
    current_time = time.time()
    for r in reminders[:]:
        if current_time >= r[0]:
            speak(f"⏰ Reminder: {r[1]}")
            reminders.remove(r)

def run_assistant():
    speak("Hello! I am your assistant. How can I help you today?")
    while True:
        command = listen()

        if "weather" in command:
            speak("Which city's weather would you like to check?")
            city = listen()
            get_weather(city)

        elif "news" in command:
            get_news()

        elif "remind me" in command:
            speak("What should I remind you about?")
            reminder_text = listen()
            if not reminder_text:
                continue

            speak("In how many minutes?")
            minutes_text = listen()

            try:
                minutes = int(minutes_text)
                set_reminder(reminder_text, minutes * 60)
            except ValueError:
                speak("That wasn't a valid number. Please try again.")

        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day!")
            break

        check_reminders()
        time.sleep(1)  # Reduce CPU usage

# Entry Point
if __name__ == "__main__":
    run_assistant()
