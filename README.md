# jarvis-ai-assistant
Advanced AI assistant inspired by Iron Man's JARVIS

## Features

- 🎤 Voice recognition and text-to-speech
- 🌐 Wikipedia search integration
- 🌤️ Weather information
- 🖥️ **Immersive Iron Man-style dashboard UI**
- 📊 Real-time system monitoring
- 🎨 Accessibility features (high contrast, font scaling)

## Quick Start

### Voice Assistant (Terminal)
```bash
# Run the voice assistant
python jarvis.txt
```

### Dashboard UI
```bash
# Launch the immersive dashboard
python scripts/run_ui.py

# Launch with mock data (for development)
python scripts/run_ui.py --mock

# Launch in headless mode (for testing)
python scripts/run_ui.py --headless
```

## Dashboard Features

The Jarvis Dashboard provides a stunning Iron Man-inspired interface with:

- **Conversation Feed**: Real-time chat history with timestamps
- **Task Status**: Live task monitoring with status indicators
- **System Metrics**: CPU, memory, disk, and network usage
- **Memory Snippets**: Key-value memory storage display
- **Waveform Visualizer**: Real-time audio visualization

### Accessibility

- **High Contrast Mode**: Toggle for improved visibility
- **Font Scaling**: Adjust text size from 0.5x to 2.0x
- **Keyboard Navigation**: Full keyboard support

## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Dependencies

- speech_recognition
- pyttsx3
- wikipedia
- requests
- wolframalpha
- PySide6 (for UI)
- psutil (for system metrics)

## Documentation

- [UI Module Documentation](ui/README.md)

## License

MIT License
