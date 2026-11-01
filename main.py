import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from google import genai
from gtts import gTTS
from dotenv import load_dotenv
import pygame
import os

# pip install pocketsphinx
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
newsapi = os.getenv("NEWS_API_KEY")
recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=command,
            config={
                "system_instruction": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Assistant. Give short responses."
            }
        )
        return response.text
    except Exception as e:  
        print("Gemini API Error:", e)
        return "Sorry, I am unable to process your request at the moment."


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    command = r.recognize_google(audio)
                    print("You said:", command)
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))