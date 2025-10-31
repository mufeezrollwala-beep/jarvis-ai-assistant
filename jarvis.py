"""
Voice interface for Jarvis assistant
"""
import speech_recognition as sr
import pyttsx3
from jarvis_core import JarvisCore


class Jarvis:
    """Voice interface for Jarvis assistant"""
    
    def __init__(self):
        self.core = JarvisCore()
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
        greeting = self.core.get_greeting()
        self.speak(greeting)

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
        """Process user commands using core logic and speak response"""
        response = self.core.process_command(query)
        
        if response['success']:
            print(response['message'])
            self.speak(response['message'])
        else:
            print(f"Error: {response['message']}")
            self.speak(response['message'])
        
        if response['action'] == 'exit':
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
