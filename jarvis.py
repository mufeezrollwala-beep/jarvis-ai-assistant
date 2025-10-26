import datetime
import webbrowser
from typing import Optional

import pyttsx3
import requests
import speech_recognition as sr
import wikipedia


class Jarvis:
    def __init__(self) -> None:
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[0].id)
        self.recognizer = sr.Recognizer()

    def speak(self, text: str) -> None:
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self) -> None:
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Jarvis. How can I help you?")

    def take_command(self) -> str:
        """Listen for commands"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query: str = self.recognizer.recognize_google(audio, language="en-US")
            print(f"User said: {query}\n")
            return query.lower()
        except Exception:
            print("Could you please repeat that?")
            return "None"

    def get_wikipedia_summary(self, query: str) -> Optional[str]:
        """Get Wikipedia summary for a query"""
        try:
            result: str = wikipedia.summary(query, sentences=2)
            return result
        except Exception:
            return None

    def get_weather(self, api_key: str, city: str) -> Optional[dict]:
        """Get weather information for a city"""
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={api_key}&q={city}"

        try:
            response = requests.get(complete_url)
            data = response.json()

            if data.get("cod") != "404":
                return {
                    "temperature": data["main"]["temp"],
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                }
        except Exception:
            pass

        return None

    def process_command(
        self, query: str, weather_api_key: str = "YOUR_WEATHER_API_KEY", city: str = "your_city"
    ) -> None:
        """Process user commands"""
        if "wikipedia" in query:
            self.speak("Searching Wikipedia...")
            search_query = query.replace("wikipedia", "").strip()
            results = self.get_wikipedia_summary(search_query)

            if results:
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            else:
                self.speak("Sorry, I couldn't find any information.")

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"The time is {str_time}")

        elif "weather" in query:
            weather_data = self.get_weather(weather_api_key, city)

            if weather_data:
                temp_celsius = weather_data["temperature"] - 273.15
                self.speak(f"Temperature is {temp_celsius:.2f} degrees Celsius")
                self.speak(f"Atmospheric pressure is {weather_data['pressure']} hPa")
                self.speak(f"Humidity is {weather_data['humidity']} percent")
            else:
                self.speak("City not found")

        elif "exit" in query:
            self.speak("Goodbye!")
            exit()


def main() -> None:
    jarvis = Jarvis()
    jarvis.wish_me()

    while True:
        query = jarvis.take_command()
        if query != "None":
            jarvis.process_command(query)


if __name__ == "__main__":
    main()
