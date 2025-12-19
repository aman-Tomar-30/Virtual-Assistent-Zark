import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from openai import OpenAI

# ================== API KEYS ==================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

# ================== INIT ==================
recogniser = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ================== AI PROCESS ==================
def aiProcess(command):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"You are Zark, a smart voice assistant. Answer briefly.\nUser: {command}"
    )

    return response.output_text

# ================== COMMAND HANDLER ==================
def processCommand(c):
    print("Command:", c)

    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
            speak(f"Playing {song}")
        else:
            speak("Sorry, song not found")

    elif "news" in c:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            speak("Here are today's top headlines")
            for article in data["articles"][:5]:
                speak(article["title"])
        else:
            speak("Unable to fetch news")

    else:
        output = aiProcess(c)
        speak(output)

# ================== MAIN LOOP ==================
if __name__ == "__main__":
    speak("Initializing Zark")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=4)

            word = recogniser.recognize_google(audio)

            if "zark" in word.lower():
                speak("Yes")

                with sr.Microphone() as source:
                    print("Zark Active...")
                    audio = recogniser.listen(source)
                    command = recogniser.recognize_google(audio)

                processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print("Error:", e)
