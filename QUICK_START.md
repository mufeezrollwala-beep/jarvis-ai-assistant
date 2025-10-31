# Quick Start Guide - Home Automation

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Test the Integration

```bash
# Run tests (uses mock devices)
python tests/test_home_automation.py

# Run demo
python demo_home_automation.py
```

## Use with Jarvis

```bash
# Start Jarvis (with mock devices by default)
python jarvis.py
```

Then say or type any of these commands:

### Lighting Commands
- "Turn on office lights"
- "Turn off bedroom lights"  
- "Turn off all lights"
- "Dim living room lights"
- "Brighten kitchen lights"

### Thermostat Commands
- "Set thermostat to 22 degrees"
- "Set thermostat to 20 degrees"
- "What's the temperature?"

### Smart Plug Commands
- "Turn on the coffee maker"
- "Turn off the coffee maker"
- "Turn on the desk lamp"
- "Turn off the desk lamp"

### Scene Commands
- "Activate movie time scene"
- "Good morning scene"
- "Good night scene"
- "Work mode scene"
- "Away mode"

### Status Commands
- "List devices"
- "Show device status"
- "Show home status"

## API Usage Example

```python
import asyncio
from home_automation import HomeAutomationService

async def main():
    # Initialize with mock devices
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    # Turn on a light
    await service.turn_on_device("office lights")
    
    # Dim a light to 50%
    await service.dim_light("living room lights", 50)
    
    # Activate a scene
    await service.activate_scene("movie time")
    
    # Get device status
    device = await service.get_device_state("light.office")
    print(f"Office lights: {device.state.value}")
    
    # Cleanup
    await service.shutdown()

asyncio.run(main())
```

## Mock Devices Available

### Lights
- Living Room Lights
- Bedroom Lights
- Office Lights
- Kitchen Lights

### Smart Plugs
- Coffee Maker
- Desk Lamp

### Other Devices
- Main Thermostat
- Porch Light (switch)
- Front Door Sensor
- Front Door Lock

### Scenes
- Movie Time - Dim living room for movies
- Good Morning - Lights on, coffee maker start
- Good Night - Turn off all, lock doors
- Work Mode - Bright office lighting
- Away Mode - Turn off everything, lock doors

## Configuration for Real Devices

See [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md) for detailed setup with real smart home devices.

Quick example for Home Assistant:

```python
from home_automation import ConfigManager

config = ConfigManager()
config.set_credential('home_assistant', 'url', 'http://192.168.1.100:8123')
config.set_credential('home_assistant', 'token', 'your_token_here')

# Then use service with real devices
service = HomeAutomationService(config_manager=config, use_mock=False)
```

## Troubleshooting

**Import errors?** Make sure you installed requirements:
```bash
pip install -r requirements.txt
```

**Jarvis not responding?** In mock mode, Jarvis initializes home automation on startup. Check console for initialization messages.

**Want to add more devices?** Edit `home_automation/mock_api.py` to add devices to the MockDeviceDatabase.

## Next Steps

1. ✓ Test with mock devices
2. Set up real smart home platform credentials
3. Connect to real devices (see HOME_AUTOMATION_GUIDE.md)
4. Create custom scenes for your home
5. Add custom adapters for new platforms

For complete documentation, see [HOME_AUTOMATION_GUIDE.md](HOME_AUTOMATION_GUIDE.md)
