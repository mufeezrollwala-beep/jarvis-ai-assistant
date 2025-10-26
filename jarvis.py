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
from memory_store import MemoryStore
from onboarding import OnboardingManager


class Jarvis:
    def __init__(self, memory_enabled: bool = True):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.recognizer = sr.Recognizer()
        
        self.memory_enabled = memory_enabled
        if memory_enabled:
            self.memory = MemoryStore()
            self.onboarding = OnboardingManager(self.memory)
            self._check_and_run_onboarding()
        else:
            self.memory = None
            self.onboarding = None

    def _check_and_run_onboarding(self):
        status = self.onboarding.check_onboarding_status()
        if not status['is_ready']:
            print("\n" + "="*50)
            print("First-time setup detected!")
            print("="*50)
            response = input("Would you like to run onboarding? (yes/no): ").strip().lower()
            if response == 'yes':
                self.onboarding.run_onboarding()
            else:
                print("Skipping onboarding. You can run it later using: python cli.py onboarding run")

    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        greeting = ""
        
        if 0 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        self.speak(greeting)
        
        if self.memory:
            user_name = self.memory.get_user_preference("user_name")
            if user_name:
                self.speak(f"Welcome back, {user_name}!")
        
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

    def _get_enhanced_context(self, query: str) -> str:
        """Retrieve memory context for better responses"""
        if not self.memory:
            return ""
        
        context = self.memory.retrieve_context(query, long_term_limit=3)
        
        context_parts = []
        
        if context.get('recent_conversation'):
            context_parts.append("Recent conversation:")
            context_parts.append(context['recent_conversation'])
        
        if context.get('relevant_memories'):
            context_parts.append("\nRelevant knowledge:")
            for mem in context['relevant_memories']:
                context_parts.append(f"- {mem['text']}")
        
        if context.get('preferences'):
            prefs = context['preferences']
            if prefs:
                context_parts.append("\nUser preferences:")
                for key, value in prefs.items():
                    context_parts.append(f"- {key}: {value}")
        
        return "\n".join(context_parts) if context_parts else ""

    def process_command(self, query):
        """Process user commands with memory integration"""
        response = ""
        
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query_text = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query_text, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
                response = results
            except Exception as e:
                error_msg = "Sorry, I couldn't find that on Wikipedia."
                self.speak(error_msg)
                response = error_msg

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            response = "Opening YouTube"
            self.speak(response)

        elif 'open google' in query:
            webbrowser.open("google.com")
            response = "Opening Google"
            self.speak(response)

        elif 'time' in query:
            time_format = "24"
            if self.memory:
                time_format = self.memory.get_user_preference("time_format") or "24"
            
            if time_format == "12":
                strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
            else:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
            
            response = f"The time is {strTime}"
            self.speak(response)

        elif 'weather' in query:
            location = "your_city"
            if self.memory:
                location = self.memory.get_user_preference("user_location") or location
            
            api_key = os.environ.get("WEATHER_API_KEY", "YOUR_WEATHER_API_KEY")
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}appid={api_key}&q={location}"
            
            try:
                response_data = requests.get(complete_url)
                x = response_data.json()
                
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_pressure = y["pressure"]
                    current_humidity = y["humidity"]
                    
                    temp_unit = "celsius"
                    if self.memory:
                        temp_unit = self.memory.get_user_preference("temperature_unit") or "celsius"
                    
                    if temp_unit == "fahrenheit":
                        temp_value = (current_temperature - 273.15) * 9/5 + 32
                        unit_str = "Fahrenheit"
                    else:
                        temp_value = current_temperature - 273.15
                        unit_str = "Celsius"
                    
                    response = f"Temperature in {location} is {temp_value:.1f} degrees {unit_str}"
                    self.speak(response)
                    self.speak(f"Humidity is {current_humidity} percent")
                else:
                    response = "City not found"
                    self.speak(response)
            except Exception as e:
                response = "Unable to fetch weather data"
                self.speak(response)

        elif 'remember' in query or 'note' in query:
            if self.memory:
                note_text = query.replace('remember', '').replace('note', '').strip()
                if note_text:
                    self.memory.long_term.add(note_text, {'category': 'user_note'})
                    response = "I'll remember that"
                    self.speak(response)
                else:
                    response = "What should I remember?"
                    self.speak(response)
            else:
                response = "Memory system is not enabled"
                self.speak(response)

        elif 'what do you remember' in query or 'recall' in query:
            if self.memory:
                context_str = self._get_enhanced_context(query)
                if context_str:
                    print("\n=== Memory Context ===")
                    print(context_str)
                    print("======================\n")
                    response = "I found some relevant memories. Check the console."
                    self.speak(response)
                else:
                    response = "I don't have any relevant memories"
                    self.speak(response)
            else:
                response = "Memory system is not enabled"
                self.speak(response)

        elif 'my name' in query:
            if self.memory:
                user_name = self.memory.get_user_preference("user_name")
                if user_name:
                    response = f"Your name is {user_name}"
                else:
                    response = "I don't know your name yet. You can tell me during onboarding."
                self.speak(response)
            else:
                response = "Memory system is not enabled"
                self.speak(response)

        elif 'exit' in query or 'goodbye' in query or 'bye' in query:
            response = "Goodbye! Have a great day!"
            self.speak(response)
            if self.memory:
                self.memory.add_task("User session ended", "Normal exit")
            exit()
        
        if self.memory and query != "None":
            self.memory.add_conversation(query, response)
        
        return response


def main():
    print("\n" + "="*50)
    print("JARVIS - AI Assistant")
    print("="*50 + "\n")
    
    try:
        jarvis = Jarvis(memory_enabled=True)
    except Exception as e:
        print(f"Warning: Failed to initialize memory system: {e}")
        print("Starting in basic mode without memory...")
        jarvis = Jarvis(memory_enabled=False)
    
    jarvis.wish_me()
    
    while True:
        query = jarvis.take_command()
        if query != 'None':
            jarvis.process_command(query)


if __name__ == "__main__":
    main()
