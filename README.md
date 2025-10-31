# Jarvis AI Assistant

Advanced AI assistant inspired by Iron Man's JARVIS, now with comprehensive home automation capabilities.

## Features

### Core Assistant Features
- **Voice Recognition**: Uses speech_recognition for natural language processing
- **Text-to-Speech**: Powered by pyttsx3 for voice responses
- **Wikipedia Integration**: Quick information lookup
- **Web Browser Control**: Open YouTube, Google, and other websites
- **Time & Weather**: Get current time and weather information
- **Wolfram Alpha**: Advanced computational queries

### Home Automation (NEW!)
- **Multi-Platform Support**: Control devices from Home Assistant, Philips Hue, TP-Link, and more
- **Natural Language Control**: Use voice commands to control your smart home
- **Device Abstractions**: Unified interface for lights, switches, plugs, thermostats, and sensors
- **Scene Management**: Create and activate complex automation scenes
- **Secure Credentials**: Encrypted storage for API keys and tokens
- **Pluggable Architecture**: Easy to add new smart home platforms
- **Mock Mode**: Test without physical devices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage
```bash
python jarvis.py
```

### Voice Commands

#### Standard Commands
- "Wikipedia [topic]" - Search Wikipedia
- "Open YouTube" - Opens YouTube in browser
- "Open Google" - Opens Google in browser
- "What time is it?" - Get current time
- "Weather" - Get weather information
- "Exit" - Quit the assistant

#### Home Automation Commands
- "Turn on office lights"
- "Turn off bedroom lights"
- "Dim living room lights"
- "Set thermostat to 22 degrees"
- "Turn on the coffee maker"
- "Activate movie time scene"
- "List devices"
- "Show home status"

## Home Automation Setup

### Mock Mode (Default)
The system runs with simulated devices by default - perfect for testing:
```python
# In jarvis.py, home automation is initialized with use_mock=True
```

### Production Mode
See [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md) for detailed setup instructions.

Quick setup for Home Assistant:
```python
from home_automation import ConfigManager

config = ConfigManager()
config.set_credential('home_assistant', 'url', 'http://your-ha-instance:8123')
config.set_credential('home_assistant', 'token', 'your_long_lived_access_token')
```

## Configuration

### Weather API
Update the weather API key in `jarvis.py`:
```python
api_key = "YOUR_OPENWEATHERMAP_API_KEY"
city = "your_city"
```

### Home Automation
Copy and customize the example configuration:
```bash
cp config.example.json ~/.jarvis/config.json
```

Edit `~/.jarvis/config.json` with your credentials.

## Architecture

### Project Structure
```
jarvis-ai-assistant/
├── jarvis.py                 # Main assistant script
├── home_automation/          # Home automation module
│   ├── __init__.py
│   ├── base.py              # Abstract base classes
│   ├── service.py           # Main service orchestrator
│   ├── config.py            # Configuration management
│   ├── mock_api.py          # Mock device database
│   └── adapters/            # Provider adapters
│       ├── __init__.py
│       ├── home_assistant.py
│       ├── hue.py
│       └── tplink.py
├── tests/                   # Test suite
│   └── test_home_automation.py
├── requirements.txt         # Python dependencies
├── config.example.json      # Example configuration
├── HOME_AUTOMATION_GUIDE.md # Detailed documentation
└── README.md               # This file
```

### Supported Device Types
- **Lights**: On/off, dimming, color temperature
- **Switches**: On/off control
- **Smart Plugs**: On/off, power monitoring
- **Thermostats**: Temperature control, mode switching
- **Sensors**: State monitoring
- **Locks**: Lock/unlock control
- **Cameras**: State monitoring (coming soon)

### Supported Platforms
- **Home Assistant**: Full REST API and WebSocket support
- **Philips Hue**: Complete light control
- **TP-Link**: Smart plug and switch control
- **Extensible**: Easy to add custom adapters

## Testing

Run the test suite:
```bash
python tests/test_home_automation.py
```

Expected output:
- Device discovery tests
- State control tests
- Scene activation tests
- Multi-adapter tests
- Natural language command tests

## Security

- **Encrypted Credentials**: All API keys stored with Fernet encryption
- **Secure Permissions**: Config files use restrictive permissions (0600)
- **No Hardcoded Secrets**: Use environment variables or encrypted config
- **HTTPS Support**: Secure communication with smart home platforms

See [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md) for detailed security guidelines.

## API Usage

```python
import asyncio
from home_automation import HomeAutomationService

async def main():
    # Initialize
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    # List devices
    devices = service.list_devices()
    print(f"Found {len(devices)} devices")
    
    # Control devices
    await service.turn_on_device("office lights")
    await service.dim_light("living room lights", 50)
    
    # Activate scene
    await service.activate_scene("movie time")
    
    # Cleanup
    await service.shutdown()

asyncio.run(main())
```

## Creating Custom Adapters

Add support for new platforms by extending `HomeAutomationAdapter`:

```python
from home_automation.base import HomeAutomationAdapter

class MyAdapter(HomeAutomationAdapter):
    async def connect(self) -> bool:
        # Connection logic
        return True
    
    async def discover_devices(self) -> List[Device]:
        # Device discovery
        return []
    
    # Implement other required methods...
```

Register with the service:
```python
service.register_adapter('my_platform', MyAdapter(config))
```

See [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md) for complete adapter development guide.

## Dependencies

- `speech_recognition` - Voice input processing
- `pyttsx3` - Text-to-speech engine
- `wikipedia` - Wikipedia API wrapper
- `requests` - HTTP client
- `wolframalpha` - Computational intelligence
- `cryptography` - Secure credential storage

## Troubleshooting

### Microphone Issues
Ensure your microphone is properly configured and accessible:
```bash
# Test microphone
python -m speech_recognition
```

### Home Automation Connection Issues
1. Check network connectivity
2. Verify credentials in config
3. Ensure smart home platform is accessible
4. Review logs for error messages

### Mock Mode Testing
Use mock mode to test without physical devices:
```python
service = HomeAutomationService(use_mock=True)
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional smart home platform adapters
- Voice recognition improvements
- New automation features
- Documentation enhancements
- Test coverage expansion

## Future Roadmap

- [ ] Real-time device state synchronization via WebSocket
- [ ] Advanced automation rules engine
- [ ] Multi-user support with profiles
- [ ] Mobile app integration
- [ ] Energy monitoring dashboard
- [ ] AI-powered automation suggestions
- [ ] Geofencing support
- [ ] Calendar integration
- [ ] Security camera feeds

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by Marvel's J.A.R.V.I.S. (Just A Rather Very Intelligent System)
- Built with open-source technologies
- Community-driven development

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md) for detailed documentation
- Review tests for usage examples

---

**Note**: This is a development version. Always test in mock mode before connecting to real smart home devices. Use at your own risk.
