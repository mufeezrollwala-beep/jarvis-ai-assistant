import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Jarvis. How can I help you?")

    def take_command(self):
        """Listen for commands"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception as e:
            print("Could you please repeat that?")
            return "None"

    def process_command(self, query):
        """Process user commands"""
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"The time is {strTime}")

        elif 'weather' in query:
            # Add your weather API key here
            api_key = "YOUR_WEATHER_API_KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city = "your_city"  # Add your city here
            complete_url = f"{base_url}appid={api_key}&q={city}"
            response = requests.get(complete_url)
            x = response.json()
            
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                self.speak(f"Temperature is {current_temperature-273.15:.2f} degrees Celsius")
                self.speak(f"Atmospheric pressure is {current_pressure} hPa")
                self.speak(f"Humidity is {current_humidity} percent")
            else:
                self.speak("City not found")

        elif 'exit' in query:
            self.speak("Goodbye!")
            exit()

def main():
    jarvis = Jarvis()
    jarvis.wish_me()
    
    while True:
        query = jarvis.take_command()
        if query != 'None':
            jarvis.process_command(query)

if __name__ == "__main__":
    main()