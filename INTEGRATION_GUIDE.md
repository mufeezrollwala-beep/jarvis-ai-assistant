# Integration Guide - Connecting Voice Assistant to Dashboard

## Overview

This guide shows how to integrate the visual dashboard with the existing Jarvis voice assistant (`jarvis.txt`).

## Architecture

```
┌─────────────────┐     Events      ┌──────────────┐
│ Voice Assistant │ ─────────────> │  Event Bus   │
│   (jarvis.txt)  │                 │  (Singleton) │
└─────────────────┘                 └──────────────┘
                                           │
                                           │ Signals
                                           ▼
                                    ┌──────────────┐
                                    │  Dashboard   │
                                    │   UI (QML)   │
                                    └──────────────┘
```

## Step-by-Step Integration

### 1. Modify the Jarvis Class

Add UI event emissions to the existing `jarvis.txt`:

```python
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

# Add UI imports
from ui.event_bus import EventBus

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.recognizer = sr.Recognizer()
        
        # Initialize event bus for UI
        self.event_bus = EventBus()
        self.event_bus.update_status("Jarvis initialized")

    def speak(self, text):
        """Convert text to speech"""
        # Emit to UI
        self.event_bus.add_conversation("Jarvis", text)
        
        # Original speak functionality
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        self.speak(greeting)
        self.speak("I am Jarvis. How can I help you?")

    def take_command(self):
        """Listen for commands"""
        with sr.Microphone() as source:
            print("Listening...")
            self.event_bus.update_status("Listening for command...")
            
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            self.event_bus.update_status("Recognizing speech...")
            self.event_bus.add_task("recognize_001", "Speech recognition", "running")
            
            query = self.recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
            
            # Emit to UI
            self.event_bus.add_conversation("User", query)
            self.event_bus.add_task("recognize_001", "Speech recognition", "completed")
            
            return query.lower()
        except Exception as e:
            print("Could you please repeat that?")
            self.event_bus.add_task("recognize_001", "Speech recognition", "failed")
            return "None"

    def process_command(self, query):
        """Process user commands"""
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            task_id = f"wiki_{int(time.time())}"
            self.event_bus.add_task(task_id, "Wikipedia search", "running")
            
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)
            
            self.event_bus.add_task(task_id, "Wikipedia search", "completed")
            self.event_bus.add_memory("Last Search", f"Wikipedia: {query}")

        elif 'open youtube' in query:
            task_id = f"youtube_{int(time.time())}"
            self.event_bus.add_task(task_id, "Open YouTube", "running")
            webbrowser.open("youtube.com")
            self.event_bus.add_task(task_id, "Open YouTube", "completed")

        elif 'open google' in query:
            task_id = f"google_{int(time.time())}"
            self.event_bus.add_task(task_id, "Open Google", "running")
            webbrowser.open("google.com")
            self.event_bus.add_task(task_id, "Open Google", "completed")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"The time is {strTime}")
            self.event_bus.add_memory("Time Check", strTime)

        elif 'weather' in query:
            api_key = "YOUR_WEATHER_API_KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city = "your_city"
            
            task_id = f"weather_{int(time.time())}"
            self.event_bus.add_task(task_id, "Fetch weather data", "running")
            
            complete_url = f"{base_url}appid={api_key}&q={city}"
            response = requests.get(complete_url)
            x = response.json()
            
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                
                temp_celsius = current_temperature - 273.15
                self.speak(f"Temperature is {temp_celsius:.2f} degrees Celsius")
                self.speak(f"Atmospheric pressure is {current_pressure} hPa")
                self.speak(f"Humidity is {current_humidity} percent")
                
                self.event_bus.add_task(task_id, "Fetch weather data", "completed")
                self.event_bus.add_memory("Weather", f"{temp_celsius:.1f}°C, {current_humidity}% humidity")
            else:
                self.speak("City not found")
                self.event_bus.add_task(task_id, "Fetch weather data", "failed")

        elif 'exit' in query:
            self.speak("Goodbye!")
            self.event_bus.update_status("Shutting down...")
            exit()
```

### 2. Create Integrated Launcher

Create a new file `jarvis_with_ui.py`:

```python
#!/usr/bin/env python3
import sys
import threading
from PySide6.QtCore import QTimer
from ui.dashboard import JarvisDashboard
from ui.event_bus import EventBus

# Import modified Jarvis class
# (Assuming you've moved jarvis.txt content to jarvis_assistant.py)
from jarvis_assistant import Jarvis


def run_voice_assistant():
    """Run voice assistant in background thread"""
    jarvis = Jarvis()
    jarvis.wish_me()
    
    while True:
        query = jarvis.take_command()
        if query != 'None':
            jarvis.process_command(query)


def main():
    print("=" * 70)
    print("  J.A.R.V.I.S - Full Integration")
    print("  Voice Assistant + Dashboard UI")
    print("=" * 70)
    print()
    
    # Start voice assistant in background thread
    assistant_thread = threading.Thread(target=run_voice_assistant, daemon=True)
    assistant_thread.start()
    print("✓ Voice assistant thread started")
    
    # Start metrics updater
    event_bus = EventBus()
    
    # Launch dashboard UI
    print("✓ Launching dashboard UI...")
    dashboard = JarvisDashboard(mock_mode=False, headless_safe=False)
    
    if dashboard.initialize():
        # Start real-time metrics
        dashboard.get_bridge().startRealMode()
        
        print("✓ Dashboard initialized")
        print()
        print("Speak 'exit' to quit")
        print("=" * 70)
        print()
        
        return dashboard.run()
    else:
        print("✗ Failed to initialize dashboard")
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

### 3. Real-Time Metrics Integration

Add a metrics updater to continuously update system stats:

```python
import psutil
import time
from PySide6.QtCore import QTimer
from ui.event_bus import EventBus


class MetricsUpdater:
    def __init__(self):
        self.event_bus = EventBus()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        
    def start(self, interval_ms=2000):
        """Start updating metrics every interval_ms milliseconds"""
        self.timer.start(interval_ms)
    
    def stop(self):
        self.timer.stop()
    
    def update_metrics(self):
        """Update system metrics"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net_io = psutil.net_io_counters()
            
            metrics = {
                'cpu': cpu,
                'memory': memory,
                'disk': disk,
                'network_in': net_io.bytes_recv / 1024 / 1024,
                'network_out': net_io.bytes_sent / 1024 / 1024,
                'uptime': time.time() - psutil.boot_time(),
            }
            
            # Try to get temperature (Linux only)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    metrics['temperature'] = list(temps.values())[0][0].current
            except:
                pass
            
            self.event_bus.update_metrics(metrics)
        except Exception as e:
            print(f"Metrics update error: {e}")


# Usage in main application
def main():
    dashboard = JarvisDashboard()
    if dashboard.initialize():
        metrics = MetricsUpdater()
        metrics.start(2000)  # Update every 2 seconds
        
        return dashboard.run()
```

### 4. Audio Waveform Visualization

Capture audio levels during listening:

```python
import numpy as np
from ui.event_bus import EventBus


def process_audio_for_visualization(audio_data):
    """Convert audio data to waveform for visualization"""
    event_bus = EventBus()
    
    # Convert audio to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Normalize to -1.0 to 1.0 range
    normalized = audio_array.astype(np.float32) / 32768.0
    
    # Downsample to 50 points for visualization
    samples = 50
    step = len(normalized) // samples
    waveform = [normalized[i * step] for i in range(samples)]
    
    # Emit to UI
    event_bus.update_audio_waveform(waveform)


# In your take_command method:
def take_command(self):
    with sr.Microphone() as source:
        audio = self.recognizer.listen(source)
        
        # Visualize audio
        process_audio_for_visualization(audio.get_raw_data())
        
        # Continue with recognition...
```

## Testing Integration

### 1. Test Event Bus
```python
from ui.event_bus import EventBus

event_bus = EventBus()
event_bus.add_conversation("User", "Test message")
event_bus.add_task("test_001", "Test task", "running")
print("Events emitted successfully")
```

### 2. Test UI with Assistant Events
```bash
# Terminal 1: Run UI
python scripts/run_ui.py

# Terminal 2: Test events
python -c "
from ui.event_bus import EventBus
import time

bus = EventBus()
bus.add_conversation('User', 'Hello Jarvis')
time.sleep(1)
bus.add_conversation('Jarvis', 'Hello, sir. How may I assist you?')
"
```

### 3. Full Integration Test
```bash
python jarvis_with_ui.py
```

## Best Practices

### 1. Thread Safety
- Always use EventBus for cross-thread communication
- Qt Signals/Slots are thread-safe
- Don't modify UI directly from assistant thread

### 2. Error Handling
```python
try:
    event_bus.add_conversation("User", message)
except Exception as e:
    print(f"UI update failed: {e}")
    # Continue without UI
```

### 3. Performance
- Update metrics no more than once per second
- Limit conversation history (auto-managed by EventBus)
- Downsample audio data before visualization

### 4. Graceful Degradation
```python
def initialize_ui():
    try:
        dashboard = JarvisDashboard()
        return dashboard if dashboard.initialize() else None
    except:
        print("Running without UI")
        return None

# Use UI only if available
dashboard = initialize_ui()
if dashboard:
    # UI available
    pass
else:
    # Run without UI
    pass
```

## Troubleshooting

### UI Not Updating
- Check EventBus singleton is being used correctly
- Verify Qt event loop is running
- Ensure dashboard.run() is called

### Audio Visualization Issues
- Check audio data format (16-bit PCM)
- Verify normalization to -1.0 to 1.0 range
- Reduce sample count if performance issues

### Thread Deadlocks
- Never call Qt UI methods from assistant thread
- Always use EventBus signals
- Use daemon threads for background tasks

## Example: Complete Integration

See `scripts/run_integrated.py` for a working example of:
- Voice assistant in background thread
- UI in main thread
- EventBus communication
- Graceful shutdown

## Next Steps

1. Test integration with mock data
2. Add real audio visualization
3. Implement more detailed task tracking
4. Add conversation context to memory
5. Create command history feature
