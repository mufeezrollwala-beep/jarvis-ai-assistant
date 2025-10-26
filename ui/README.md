# Jarvis Dashboard UI

An immersive Iron Man/Jarvis-inspired desktop interface for the Jarvis AI assistant.

## Features

- **Real-time Updates**: Event-driven architecture with WebSocket-ready event bus
- **Mock Data Mode**: Development mode with realistic animated data
- **Accessibility**: High contrast mode and font scaling (0.5x - 2.0x)
- **Iron Man Aesthetic**: Neon cyan accents, animated backgrounds, glowing elements
- **Performance**: Optimized animations and efficient rendering
- **Graceful Degradation**: Headless mode support for testing

## Panels

### 1. Conversation Feed
- Real-time chat history between user and Jarvis
- Color-coded speakers (User: cyan, Jarvis: green)
- Timestamps and smooth animations

### 2. Task Status
- Active and completed tasks
- Status indicators (pending, running, completed)
- Task descriptions and timestamps

### 3. System Metrics
- CPU, Memory, Disk usage
- Network I/O statistics
- Real-time graphs with animated progress bars

### 4. Memory Snippets
- Key-value memory items
- User preferences and system notes
- Chronological display with timestamps

### 5. Waveform Visualizer
- Real-time audio waveform display
- Animated particle effects
- "LIVE" indicator with pulse animation

## Usage

### Launch with Real-time Data
```bash
python scripts/run_ui.py
```

### Launch with Mock Data (Development)
```bash
python scripts/run_ui.py --mock
```

### Launch in Headless Mode
```bash
python scripts/run_ui.py --headless
```

## Accessibility Features

### High Contrast Mode
- Toggle via the "High Contrast" button in the top bar
- Switches to black background with yellow accents
- Improved visibility for visually impaired users

### Font Scaling
- Use "A-" and "A+" buttons to adjust font size
- Range: 0.5x to 2.0x
- Scales all text throughout the interface

## Integration

To integrate with the voice assistant:

```python
from ui.event_bus import EventBus

# Get the event bus instance
event_bus = EventBus()

# Add conversation entries
event_bus.add_conversation("User", "What's the weather?")
event_bus.add_conversation("Jarvis", "It's 72°F and sunny.")

# Add tasks
event_bus.add_task("task_001", "Fetch weather data", "completed")

# Update metrics
metrics = {
    'cpu': 45.2,
    'memory': 62.8,
    'disk': 55.0,
    'network_in': 1024.5,
    'network_out': 512.3
}
event_bus.update_metrics(metrics)

# Add memory items
event_bus.add_memory("User Preference", "Prefers Celsius")

# Update audio waveform
waveform_data = [0.1, 0.3, 0.5, 0.3, 0.1, ...]  # List of floats
event_bus.update_audio_waveform(waveform_data)
```

## Architecture

### Event Bus (`event_bus.py`)
- Singleton pattern for global access
- Qt Signal/Slot mechanism for thread-safe updates
- Maintains history of conversations, tasks, and memory

### Dashboard Bridge (`dashboard.py`)
- Connects Python backend to QML frontend
- Exposes data as Qt Properties
- Handles accessibility settings

### Mock Data Generator (`mock_data.py`)
- Threaded background generator
- Realistic simulation of assistant activity
- Useful for UI development and testing

## Theme

The theme is defined in `qml/Theme.qml` with Iron Man-inspired colors:

- **Primary**: Cyan (`#00d9ff`)
- **Secondary**: Blue (`#0099cc`)
- **Accent**: Bright cyan (`#00ffff`)
- **Success**: Green (`#00ff88`)
- **Warning**: Orange (`#ffaa00`)
- **Error**: Red (`#ff3366`)

All colors feature glow effects and smooth animations when appropriate.

## Requirements

- PySide6 >= 6.10.0
- psutil >= 7.1.0
- Python >= 3.9

## License

Part of the Jarvis AI Assistant project.
