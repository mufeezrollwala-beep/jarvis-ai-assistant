import random
import time
import math
from datetime import datetime
from PySide6.QtCore import QThread, Signal
from typing import List


class MockDataGenerator(QThread):
    conversation_signal = Signal(str, str)
    task_signal = Signal(str, str, str)
    metrics_signal = Signal(dict)
    memory_signal = Signal(str, str)
    audio_signal = Signal(list)
    status_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._running = False
        self._tick_count = 0
        
        self.mock_conversations = [
            ("User", "What's the weather today?"),
            ("Jarvis", "The current temperature is 72°F with clear skies."),
            ("User", "Open YouTube"),
            ("Jarvis", "Opening YouTube now, sir."),
            ("User", "Tell me about quantum computing"),
            ("Jarvis", "Quantum computing uses quantum-mechanical phenomena..."),
            ("User", "What time is it?"),
            ("Jarvis", "The current time is {}"),
            ("User", "Search Wikipedia for artificial intelligence"),
            ("Jarvis", "Searching Wikipedia for artificial intelligence..."),
            ("User", "Play some music"),
            ("Jarvis", "Playing your favorite playlist, sir."),
            ("User", "What are my tasks for today?"),
            ("Jarvis", "You have 3 pending tasks in your schedule."),
        ]
        
        self.mock_tasks = [
            ("task_001", "Process Wikipedia query", ["pending", "running", "completed"]),
            ("task_002", "Fetch weather data", ["pending", "running", "completed"]),
            ("task_003", "Open browser application", ["pending", "completed"]),
            ("task_004", "Speech recognition active", ["running"]),
            ("task_005", "Analyze voice command", ["pending", "running", "completed"]),
            ("task_006", "System diagnostics", ["running", "completed"]),
        ]
        
        self.mock_memories = [
            ("User Preference", "Prefers morning greetings"),
            ("Last Command", "Weather query at 09:45 AM"),
            ("Favorite Site", "YouTube"),
            ("Common Query", "Time check - 15 times today"),
            ("Voice Pattern", "Recognition accuracy: 98.5%"),
            ("System Note", "All systems operational"),
        ]
        
    def run(self):
        self._running = True
        self.status_signal.emit("Mock data generator started")
        
        while self._running:
            self._tick_count += 1
            
            if self._tick_count % 3 == 0:
                self._generate_conversation()
            
            if self._tick_count % 5 == 0:
                self._generate_task()
            
            if self._tick_count % 2 == 0:
                self._generate_metrics()
            
            if self._tick_count % 7 == 0:
                self._generate_memory()
            
            self._generate_audio_waveform()
            
            time.sleep(2)
    
    def _generate_conversation(self):
        speaker, message = random.choice(self.mock_conversations)
        if "{}" in message:
            message = message.format(datetime.now().strftime("%H:%M:%S"))
        self.conversation_signal.emit(speaker, message)
    
    def _generate_task(self):
        task_id, description, statuses = random.choice(self.mock_tasks)
        status = random.choice(statuses)
        unique_id = f"{task_id}_{self._tick_count}"
        self.task_signal.emit(unique_id, description, status)
    
    def _generate_metrics(self):
        metrics = {
            'cpu': random.uniform(20, 80),
            'memory': random.uniform(30, 70),
            'disk': random.uniform(40, 60),
            'network_in': random.uniform(100, 5000),
            'network_out': random.uniform(50, 2000),
            'temperature': random.uniform(45, 75),
            'uptime': time.time() % 86400,
        }
        self.metrics_signal.emit(metrics)
    
    def _generate_memory(self):
        key, value = random.choice(self.mock_memories)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.memory_signal.emit(key, f"{value} - {timestamp}")
    
    def _generate_audio_waveform(self):
        t = time.time()
        samples = 50
        waveform = []
        
        for i in range(samples):
            phase = (t * 2 + i / samples * 4 * math.pi) % (2 * math.pi)
            value = (
                math.sin(phase) * 0.4 +
                math.sin(phase * 2.5) * 0.3 +
                math.sin(phase * 5) * 0.2 +
                random.uniform(-0.1, 0.1)
            )
            waveform.append(value)
        
        self.audio_signal.emit(waveform)
    
    def stop(self):
        self._running = False
        self.status_signal.emit("Mock data generator stopped")
