import asyncio
import datetime
import wikipedia
import webbrowser
import requests
from typing import Optional
from src.task_manager import TaskManager, TaskState, Task
from src.background_actions import download_file, reminder_timer, periodic_health_check, batch_web_search


class JarvisCLI:
    def __init__(self):
        self.task_manager = TaskManager(max_concurrent_tasks=5)
        self.task_manager.add_event_callback(self.on_task_event)
        self.running = False
        
    def print_message(self, text):
        print(f"[JARVIS]: {text}")

    def greet(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.print_message("Good Morning!")
        elif 12 <= hour < 18:
            self.print_message("Good Afternoon!")
        else:
            self.print_message("Good Evening!")
        self.print_message("I am Jarvis. How can I help you? (Type 'help' for commands)")
    
    async def on_task_event(self, task: Task, event_type: str):
        if event_type == "started":
            self.print_message(f"Task '{task.name}' started (ID: {task.id[:8]})")
        elif event_type == "completed":
            self.print_message(f"Task '{task.name}' completed successfully")
            if task.result:
                print(f"  Result: {task.result}")
        elif event_type == "failed":
            self.print_message(f"Task '{task.name}' failed: {task.error}")
        elif event_type == "cancelled":
            self.print_message(f"Task '{task.name}' cancelled")

    def show_help(self):
        help_text = """
Available Commands:
  help                    - Show this help message
  wikipedia <query>       - Search Wikipedia
  open youtube            - Open YouTube
  open google             - Open Google
  time                    - Get current time
  weather                 - Get weather information
  
Task Management:
  download test           - Download a test file
  reminder <seconds>      - Set a reminder timer
  health check            - Start periodic health check
  list tasks              - List all tasks
  cancel task             - Cancel a task
  task status             - Show running task status
  
  exit/quit               - Exit Jarvis
        """
        print(help_text)

    async def process_command(self, query: str):
        query = query.lower().strip()
        
        if not query or query == "none":
            return
        
        if query == 'help':
            self.show_help()
            
        elif 'wikipedia' in query:
            self.print_message('Searching Wikipedia...')
            search_query = query.replace("wikipedia", "").strip()
            if search_query:
                try:
                    results = wikipedia.summary(search_query, sentences=2)
                    self.print_message("According to Wikipedia:")
                    print(results)
                except Exception as e:
                    self.print_message(f"Error searching Wikipedia: {e}")
            else:
                self.print_message("Please provide a search query")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            self.print_message("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("google.com")
            self.print_message("Opening Google")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.print_message(f"The time is {strTime}")

        elif 'weather' in query:
            api_key = "YOUR_WEATHER_API_KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city = "your_city"
            complete_url = f"{base_url}appid={api_key}&q={city}"
            
            try:
                response = requests.get(complete_url)
                x = response.json()
                
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_pressure = y["pressure"]
                    current_humidity = y["humidity"]
                    self.print_message(f"Temperature is {current_temperature-273.15:.2f} degrees Celsius")
                    self.print_message(f"Atmospheric pressure is {current_pressure} hPa")
                    self.print_message(f"Humidity is {current_humidity} percent")
                else:
                    self.print_message("City not found")
            except Exception as e:
                self.print_message(f"Error fetching weather: {e}")
        
        elif 'download' in query and ('file' in query or 'test' in query):
            url = "https://httpbin.org/bytes/10240"
            destination = "./downloads/test_file.bin"
            
            async def download_wrapper(task):
                return await download_file(task, url, destination)
            
            task_id = self.task_manager.create_task("File Download", download_wrapper, priority=5)
            self.print_message(f"File download task created (ID: {task_id[:8]})")
            
        elif 'reminder' in query:
            try:
                parts = query.split()
                seconds = None
                for part in parts:
                    if part.isdigit():
                        seconds = int(part)
                        break
                
                if seconds is None:
                    seconds = 10
                
                message = "Time's up!"
                
                async def reminder_wrapper(task):
                    return await reminder_timer(task, seconds, message)
                
                task_id = self.task_manager.create_task(f"Reminder ({seconds}s)", reminder_wrapper, priority=3)
                self.print_message(f"Reminder set for {seconds} seconds (ID: {task_id[:8]})")
            except Exception as e:
                self.print_message(f"Could not set reminder: {e}")
        
        elif 'health check' in query:
            url = "https://httpbin.org/status/200"
            
            async def health_check_wrapper(task):
                return await periodic_health_check(task, url, interval_seconds=5, max_checks=3)
            
            task_id = self.task_manager.create_task("Health Check", health_check_wrapper, priority=2)
            self.print_message(f"Health check task started (ID: {task_id[:8]})")
        
        elif 'list tasks' in query or 'show tasks' in query:
            stats = self.task_manager.get_stats()
            tasks = self.task_manager.list_tasks()
            
            if not tasks:
                self.print_message("No tasks found")
            else:
                self.print_message(f"Total: {stats['total']} | Running: {stats['running']} | "
                                 f"Pending: {stats['pending']} | Completed: {stats['completed']} | "
                                 f"Failed: {stats['failed']} | Cancelled: {stats['cancelled']}")
                
                print("\nTask Details:")
                print(f"{'ID':<10} {'Name':<20} {'State':<12} {'Progress':<10} {'Created':<20}")
                print("-" * 80)
                for task in tasks:
                    created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{task.id[:8]:<10} {task.name[:20]:<20} {task.state.value:<12} "
                          f"{task.progress:>6.1f}% {created:<20}")
        
        elif 'cancel task' in query:
            parts = query.split()
            task_id = None
            
            for i, part in enumerate(parts):
                if part == 'task' and i + 1 < len(parts):
                    task_id = parts[i + 1]
                    break
            
            if task_id:
                matching_tasks = [t for t in self.task_manager.list_tasks() 
                                if t.id.startswith(task_id)]
                if matching_tasks:
                    task = matching_tasks[0]
                    if self.task_manager.cancel_task(task.id):
                        self.print_message(f"Cancelled task '{task.name}'")
                    else:
                        self.print_message("Could not cancel task")
                else:
                    self.print_message(f"Task with ID {task_id} not found")
            else:
                pending_tasks = self.task_manager.list_tasks(TaskState.PENDING)
                running_tasks = self.task_manager.list_tasks(TaskState.RUNNING)
                
                cancelable = pending_tasks + running_tasks
                
                if cancelable:
                    task_to_cancel = cancelable[0]
                    if self.task_manager.cancel_task(task_to_cancel.id):
                        self.print_message(f"Cancelled task '{task_to_cancel.name}'")
                    else:
                        self.print_message("Could not cancel task")
                else:
                    self.print_message("No tasks to cancel")
        
        elif 'task status' in query or 'task progress' in query:
            running = self.task_manager.list_tasks(TaskState.RUNNING)
            pending = self.task_manager.list_tasks(TaskState.PENDING)
            
            if not running and not pending:
                self.print_message("No tasks currently running or pending")
            else:
                if running:
                    self.print_message("Running tasks:")
                    for task in running:
                        print(f"  - {task.name}: {task.progress:.1f}% complete")
                if pending:
                    self.print_message(f"\nPending tasks: {len(pending)}")
                    for task in pending[:3]:
                        print(f"  - {task.name} (Priority: {task.priority})")

        elif query in ['exit', 'quit', 'bye']:
            self.print_message("Shutting down. Goodbye!")
            self.running = False
            self.task_manager.stop()
        
        else:
            self.print_message("I didn't understand that command. Type 'help' for available commands.")

    async def run(self):
        self.running = True
        self.greet()
        
        task_runner = asyncio.create_task(self.task_manager.run_tasks())
        
        try:
            while self.running:
                try:
                    query = await asyncio.get_event_loop().run_in_executor(
                        None, input, "\n[You]: "
                    )
                    await self.process_command(query)
                except EOFError:
                    break
                except KeyboardInterrupt:
                    self.print_message("\nReceived interrupt signal")
                    break
                
                await asyncio.sleep(0.1)
        finally:
            self.print_message("Stopping task manager...")
            self.task_manager.stop()
            try:
                await asyncio.wait_for(task_runner, timeout=5.0)
            except asyncio.TimeoutError:
                task_runner.cancel()
                self.print_message("Forced shutdown of task runner")


async def main():
    jarvis = JarvisCLI()
    await jarvis.run()


if __name__ == "__main__":
    asyncio.run(main())
