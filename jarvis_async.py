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
from typing import Optional
from src.task_manager import TaskManager, TaskState, Task
from src.background_actions import download_file, reminder_timer, periodic_health_check, batch_web_search


class JarvisAsync:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.recognizer = sr.Recognizer()
        self.task_manager = TaskManager(max_concurrent_tasks=5)
        self.task_manager.add_event_callback(self.on_task_event)
        self.running = False
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Jarvis. How can I help you?")

    def take_command(self):
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
    
    async def on_task_event(self, task: Task, event_type: str):
        if event_type == "started":
            print(f"Task '{task.name}' started")
            self.speak(f"Task {task.name} started")
        elif event_type == "completed":
            print(f"Task '{task.name}' completed")
            self.speak(f"Task {task.name} completed successfully")
        elif event_type == "failed":
            print(f"Task '{task.name}' failed: {task.error}")
            self.speak(f"Task {task.name} failed")
        elif event_type == "cancelled":
            print(f"Task '{task.name}' cancelled")
            self.speak(f"Task {task.name} cancelled")

    async def process_command(self, query: str):
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
        
        elif 'download file' in query or 'download test' in query:
            url = "https://httpbin.org/bytes/1024"
            destination = "./downloads/test_file.bin"
            
            async def download_wrapper(task):
                return await download_file(task, url, destination)
            
            task_id = self.task_manager.create_task("File Download", download_wrapper, priority=5)
            self.speak(f"File download task created with ID {task_id[:8]}")
            
        elif 'set reminder' in query or 'reminder' in query:
            try:
                if 'seconds' in query:
                    parts = query.split()
                    seconds = int([p for p in parts if p.isdigit()][0])
                else:
                    seconds = 10
                
                message = "Time's up!"
                
                async def reminder_wrapper(task):
                    return await reminder_timer(task, seconds, message)
                
                task_id = self.task_manager.create_task(f"Reminder ({seconds}s)", reminder_wrapper, priority=3)
                self.speak(f"Reminder set for {seconds} seconds")
            except Exception as e:
                self.speak("Could not set reminder. Please specify duration in seconds.")
        
        elif 'health check' in query:
            url = "https://httpbin.org/status/200"
            
            async def health_check_wrapper(task):
                return await periodic_health_check(task, url, interval_seconds=5, max_checks=3)
            
            task_id = self.task_manager.create_task("Health Check", health_check_wrapper, priority=2)
            self.speak("Health check task started")
        
        elif 'list tasks' in query or 'show tasks' in query:
            stats = self.task_manager.get_stats()
            tasks = self.task_manager.list_tasks()
            
            if not tasks:
                self.speak("No tasks found")
            else:
                summary = f"Total tasks: {stats['total']}. "
                summary += f"Running: {stats['running']}. "
                summary += f"Pending: {stats['pending']}. "
                summary += f"Completed: {stats['completed']}"
                
                print(summary)
                self.speak(summary)
                
                print("\nTask Details:")
                for task in tasks[:5]:
                    status_line = f"- {task.name}: {task.state.value} ({task.progress:.1f}%)"
                    print(status_line)
        
        elif 'cancel task' in query:
            pending_tasks = self.task_manager.list_tasks(TaskState.PENDING)
            running_tasks = self.task_manager.list_tasks(TaskState.RUNNING)
            
            cancelable = pending_tasks + running_tasks
            
            if cancelable:
                task_to_cancel = cancelable[0]
                if self.task_manager.cancel_task(task_to_cancel.id):
                    self.speak(f"Cancelled task {task_to_cancel.name}")
                else:
                    self.speak("Could not cancel task")
            else:
                self.speak("No tasks to cancel")
        
        elif 'task status' in query or 'task progress' in query:
            running = self.task_manager.list_tasks(TaskState.RUNNING)
            
            if not running:
                self.speak("No tasks currently running")
            else:
                for task in running:
                    status = f"{task.name} is {task.progress:.1f} percent complete"
                    print(status)
                    self.speak(status)

        elif 'exit' in query or 'quit' in query:
            self.speak("Shutting down. Goodbye!")
            self.running = False
            self.task_manager.stop()

    async def run(self):
        self.running = True
        self.wish_me()
        
        task_runner = asyncio.create_task(self.task_manager.run_tasks())
        
        try:
            while self.running:
                query = await asyncio.get_event_loop().run_in_executor(None, self.take_command)
                
                if query != 'None':
                    await self.process_command(query)
                
                await asyncio.sleep(0.1)
        finally:
            self.task_manager.stop()
            try:
                await asyncio.wait_for(task_runner, timeout=5.0)
            except asyncio.TimeoutError:
                task_runner.cancel()


async def main():
    jarvis = JarvisAsync()
    await jarvis.run()


if __name__ == "__main__":
    asyncio.run(main())
