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
import asyncio
from home_automation import HomeAutomationService, DeviceType, DeviceState

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.recognizer = sr.Recognizer()
        self.home_automation = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._initialize_home_automation()

    def _initialize_home_automation(self):
        try:
            self.home_automation = HomeAutomationService(use_mock=True)
            self.loop.run_until_complete(self.home_automation.initialize())
            print("[Jarvis] Home automation initialized successfully")
        except Exception as e:
            print(f"[Jarvis] Failed to initialize home automation: {e}")
            self.home_automation = None

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
            api_key = "YOUR_WEATHER_API_KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city = "your_city"
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

        elif 'exit' in query or 'quit' in query:
            self.speak("Goodbye!")
            if self.home_automation:
                self.loop.run_until_complete(self.home_automation.shutdown())
            exit()
        
        elif self.home_automation and ('light' in query or 'lights' in query):
            self._handle_light_command(query)
        
        elif self.home_automation and 'thermostat' in query:
            self._handle_thermostat_command(query)
        
        elif self.home_automation and ('plug' in query or 'coffee' in query):
            self._handle_plug_command(query)
        
        elif self.home_automation and 'scene' in query:
            self._handle_scene_command(query)
        
        elif self.home_automation and ('list devices' in query or 'show devices' in query):
            self._list_devices()
        
        elif self.home_automation and ('device status' in query or 'home status' in query):
            self._show_home_status()

    def _handle_light_command(self, query):
        try:
            if 'turn on' in query:
                if 'office' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('office lights')
                    )
                    if success:
                        self.speak("Turning on office lights")
                elif 'bedroom' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('bedroom lights')
                    )
                    if success:
                        self.speak("Turning on bedroom lights")
                elif 'living room' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('living room lights')
                    )
                    if success:
                        self.speak("Turning on living room lights")
                elif 'kitchen' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('kitchen lights')
                    )
                    if success:
                        self.speak("Turning on kitchen lights")
                else:
                    self.speak("Which lights would you like to turn on?")
            
            elif 'turn off' in query:
                if 'office' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('office lights')
                    )
                    if success:
                        self.speak("Turning off office lights")
                elif 'bedroom' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('bedroom lights')
                    )
                    if success:
                        self.speak("Turning off bedroom lights")
                elif 'living room' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('living room lights')
                    )
                    if success:
                        self.speak("Turning off living room lights")
                elif 'kitchen' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('kitchen lights')
                    )
                    if success:
                        self.speak("Turning off kitchen lights")
                elif 'all' in query:
                    lights = self.home_automation.list_devices(device_type=DeviceType.LIGHT)
                    for light in lights:
                        self.loop.run_until_complete(
                            self.home_automation.turn_off_device(light.device_id)
                        )
                    self.speak("Turning off all lights")
                else:
                    self.speak("Which lights would you like to turn off?")
            
            elif 'dim' in query:
                if 'office' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.dim_light('office lights', 30)
                    )
                    if success:
                        self.speak("Dimming office lights")
                elif 'living room' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.dim_light('living room lights', 30)
                    )
                    if success:
                        self.speak("Dimming living room lights")
                else:
                    self.speak("Which lights would you like to dim?")
            
            elif 'brighten' in query or 'bright' in query:
                if 'office' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.dim_light('office lights', 100)
                    )
                    if success:
                        self.speak("Brightening office lights")
                elif 'living room' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.dim_light('living room lights', 100)
                    )
                    if success:
                        self.speak("Brightening living room lights")
                else:
                    self.speak("Which lights would you like to brighten?")
        
        except Exception as e:
            print(f"[Jarvis] Light command error: {e}")
            self.speak("Sorry, I had trouble controlling the lights")

    def _handle_thermostat_command(self, query):
        try:
            if 'set' in query or 'temperature' in query:
                if '20' in query or 'twenty' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.set_thermostat_temperature('main thermostat', 20)
                    )
                    if success:
                        self.speak("Setting thermostat to 20 degrees")
                elif '22' in query or 'twenty two' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.set_thermostat_temperature('main thermostat', 22)
                    )
                    if success:
                        self.speak("Setting thermostat to 22 degrees")
                elif '18' in query or 'eighteen' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.set_thermostat_temperature('main thermostat', 18)
                    )
                    if success:
                        self.speak("Setting thermostat to 18 degrees")
                else:
                    self.speak("What temperature would you like?")
            else:
                device = self.home_automation.find_device_by_name('main thermostat')
                if device:
                    temp = device.attributes.get('current_temperature', 'unknown')
                    target = device.attributes.get('target_temperature', 'unknown')
                    self.speak(f"Current temperature is {temp} degrees, target is {target} degrees")
        
        except Exception as e:
            print(f"[Jarvis] Thermostat command error: {e}")
            self.speak("Sorry, I had trouble controlling the thermostat")

    def _handle_plug_command(self, query):
        try:
            if 'coffee' in query:
                if 'turn on' in query or 'start' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('coffee maker')
                    )
                    if success:
                        self.speak("Starting the coffee maker")
                elif 'turn off' in query or 'stop' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('coffee maker')
                    )
                    if success:
                        self.speak("Turning off the coffee maker")
            elif 'desk lamp' in query:
                if 'turn on' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_on_device('desk lamp')
                    )
                    if success:
                        self.speak("Turning on the desk lamp")
                elif 'turn off' in query:
                    success = self.loop.run_until_complete(
                        self.home_automation.turn_off_device('desk lamp')
                    )
                    if success:
                        self.speak("Turning off the desk lamp")
        
        except Exception as e:
            print(f"[Jarvis] Plug command error: {e}")
            self.speak("Sorry, I had trouble controlling that device")

    def _handle_scene_command(self, query):
        try:
            if 'movie' in query:
                success = self.loop.run_until_complete(
                    self.home_automation.activate_scene('movie time')
                )
                if success:
                    self.speak("Activating movie time scene")
            elif 'good morning' in query or 'morning' in query:
                success = self.loop.run_until_complete(
                    self.home_automation.activate_scene('good morning')
                )
                if success:
                    self.speak("Activating good morning scene")
            elif 'good night' in query or 'night' in query:
                success = self.loop.run_until_complete(
                    self.home_automation.activate_scene('good night')
                )
                if success:
                    self.speak("Activating good night scene")
            elif 'work' in query:
                success = self.loop.run_until_complete(
                    self.home_automation.activate_scene('work mode')
                )
                if success:
                    self.speak("Activating work mode scene")
            elif 'away' in query:
                success = self.loop.run_until_complete(
                    self.home_automation.activate_scene('away')
                )
                if success:
                    self.speak("Activating away mode")
            else:
                scenes = self.home_automation.list_scenes()
                if scenes:
                    scene_names = ", ".join([s.name for s in scenes])
                    self.speak(f"Available scenes are: {scene_names}")
        
        except Exception as e:
            print(f"[Jarvis] Scene command error: {e}")
            self.speak("Sorry, I had trouble activating that scene")

    def _list_devices(self):
        try:
            devices = self.home_automation.list_devices()
            if devices:
                device_count = len(devices)
                lights = len([d for d in devices if d.device_type == DeviceType.LIGHT])
                plugs = len([d for d in devices if d.device_type == DeviceType.PLUG])
                self.speak(f"I found {device_count} devices. {lights} lights and {plugs} smart plugs")
                print(self.home_automation.get_device_summary())
            else:
                self.speak("No devices found")
        
        except Exception as e:
            print(f"[Jarvis] List devices error: {e}")
            self.speak("Sorry, I had trouble listing the devices")

    def _show_home_status(self):
        try:
            summary = self.home_automation.get_device_summary()
            print(summary)
            self.speak("Device status printed to console")
        except Exception as e:
            print(f"[Jarvis] Show status error: {e}")
            self.speak("Sorry, I had trouble getting the device status")

def main():
    jarvis = Jarvis()
    jarvis.wish_me()
    
    while True:
        query = jarvis.take_command()
        if query != 'None':
            jarvis.process_command(query)

if __name__ == "__main__":
    main()
