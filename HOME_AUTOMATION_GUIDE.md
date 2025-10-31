# Home Automation Integration Guide

## Overview

Jarvis now includes a comprehensive home automation integration layer that allows you to control smart home devices using natural language voice commands. The system supports multiple providers through a pluggable adapter architecture.

## Supported Providers

### 1. Home Assistant
- **Protocol**: REST API and WebSocket
- **Features**: Full device control, scenes, automations
- **Setup**: Requires Home Assistant instance URL and long-lived access token

### 2. Philips Hue
- **Protocol**: REST API
- **Features**: Light control, color/brightness, scenes
- **Setup**: Requires Hue Bridge IP and API username/key

### 3. TP-Link Smart Devices
- **Protocol**: Cloud API
- **Features**: Smart plugs, switches, power monitoring
- **Setup**: Requires TP-Link account credentials

## Architecture

### Core Components

#### HomeAutomationService
Main service orchestrating all adapters and providing unified interface for device control.

```python
from home_automation import HomeAutomationService

service = HomeAutomationService(use_mock=True)
await service.initialize()
```

#### HomeAutomationAdapter (Abstract Base)
Base class for all provider adapters. Implements:
- Device discovery
- State management
- Scene activation
- Caching layer

#### Device Abstraction
Unified device representation across all providers:
```python
class Device:
    - device_id: str
    - name: str
    - device_type: DeviceType (LIGHT, SWITCH, PLUG, THERMOSTAT, etc.)
    - state: DeviceState (ON, OFF, UNAVAILABLE, UNKNOWN)
    - attributes: Dict[str, Any]
    - room: Optional[str]
```

#### Scene Abstraction
Group multiple device states into reusable scenes:
```python
class Scene:
    - scene_id: str
    - name: str
    - description: str
    - devices: List[str]
```

## Configuration

### Mock Mode (Development/Testing)
By default, the system runs in mock mode with simulated devices:

```python
service = HomeAutomationService(use_mock=True)
```

### Production Mode
For real device control, configure credentials:

1. Create configuration directory:
```bash
mkdir -p ~/.jarvis
```

2. Set up credentials (encrypted automatically):
```python
from home_automation import ConfigManager

config = ConfigManager()

# Home Assistant
config.set_credential('home_assistant', 'url', 'http://192.168.1.100:8123')
config.set_credential('home_assistant', 'token', 'your_long_lived_token')

# Philips Hue
config.set_credential('hue', 'bridge_ip', '192.168.1.101')
config.set_credential('hue', 'username', 'your_hue_username')

# TP-Link
config.set_credential('tplink', 'username', 'your_tplink_email')
config.set_credential('tplink', 'password', 'your_tplink_password')
```

3. Initialize service:
```python
service = HomeAutomationService(config_manager=config, use_mock=False)
await service.initialize()
```

## Voice Commands

### Lighting Control
- "Turn on office lights"
- "Turn off bedroom lights"
- "Dim living room lights"
- "Brighten kitchen lights"
- "Turn off all lights"

### Thermostat Control
- "Set thermostat to 22 degrees"
- "What's the temperature?"

### Smart Plug Control
- "Turn on the coffee maker"
- "Turn off the desk lamp"

### Scene Activation
- "Activate movie time scene"
- "Good morning scene"
- "Good night scene"
- "Work mode scene"
- "Away mode"

### Device Status
- "List devices"
- "Show device status"
- "Show home status"

## API Usage

### Basic Operations

```python
import asyncio
from home_automation import HomeAutomationService

async def main():
    # Initialize service
    service = HomeAutomationService(use_mock=True)
    await service.initialize()
    
    # List all devices
    devices = service.list_devices()
    for device in devices:
        print(f"{device.name}: {device.state.value}")
    
    # Control specific device
    await service.turn_on_device("office lights")
    await service.dim_light("living room lights", brightness=50)
    await service.turn_off_device("bedroom lights")
    
    # Control by room
    await service.turn_off_room("kitchen")
    await service.turn_on_room("office")
    
    # Activate scene
    await service.activate_scene("movie time")
    
    # Get device state
    device = await service.get_device_state("light.office")
    print(f"Brightness: {device.attributes.get('brightness')}")
    
    # Cleanup
    await service.shutdown()

asyncio.run(main())
```

### Filtering Devices

```python
# By type
lights = service.list_devices(device_type=DeviceType.LIGHT)
plugs = service.list_devices(device_type=DeviceType.PLUG)

# By room
office_devices = service.list_devices(room="Office")

# By name
device = service.find_device_by_name("coffee maker")
```

### Scene Management

```python
# List scenes
scenes = service.list_scenes()
for scene in scenes:
    print(f"{scene.name}: {scene.description}")

# Activate scene
await service.activate_scene("good morning")

# Find scene by name
scene = service.find_scene_by_name("movie time")
```

## Creating Custom Adapters

To add support for new smart home platforms:

1. Create adapter class inheriting from `HomeAutomationAdapter`:

```python
from home_automation.base import HomeAutomationAdapter, Device, DeviceType, DeviceState

class MyCustomAdapter(HomeAutomationAdapter):
    def __init__(self, config: Dict[str, Any], use_mock: bool = False):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.use_mock = use_mock
    
    async def connect(self) -> bool:
        # Implement connection logic
        return True
    
    async def disconnect(self) -> None:
        # Implement disconnection logic
        pass
    
    async def discover_devices(self) -> List[Device]:
        # Implement device discovery
        devices = []
        # ... fetch devices from API
        self.cache_devices(devices)
        return devices
    
    async def get_device_state(self, device_id: str) -> Optional[Device]:
        # Implement state retrieval
        return self.get_cached_device(device_id)
    
    async def set_device_state(self, device_id: str, state: DeviceState, **kwargs) -> bool:
        # Implement state control
        return True
    
    async def get_scenes(self) -> List[Scene]:
        # Implement scene listing
        return []
    
    async def activate_scene(self, scene_id: str) -> bool:
        # Implement scene activation
        return False
```

2. Register adapter with service:

```python
from my_adapters import MyCustomAdapter

adapter = MyCustomAdapter({'api_key': 'xxx'})
service.register_adapter('my_platform', adapter)
await adapter.connect()
```

## Security Considerations

### Credential Storage
- All credentials are encrypted using Fernet (symmetric encryption)
- Encryption key stored in `~/.jarvis/.key` with restricted permissions (0600)
- Credentials stored in `~/.jarvis/credentials.enc`

### Network Security
- Use HTTPS for all API communications in production
- Validate SSL certificates
- Use long-lived tokens instead of passwords when possible
- Implement token rotation for long-running instances

### Access Control
- Limit network access to trusted devices
- Use firewall rules to restrict smart home API access
- Consider using VPN for remote access
- Enable two-factor authentication on all platforms

### Best Practices
1. Never commit credentials to version control
2. Use environment variables for sensitive data
3. Regularly rotate API keys and tokens
4. Monitor device access logs
5. Keep all software updated

## Testing

### Run Mock Tests
```bash
python tests/test_home_automation.py
```

### Test Individual Components
```python
# Test single adapter
from home_automation.adapters import HomeAssistantAdapter

adapter = HomeAssistantAdapter({'url': 'http://localhost:8123'}, use_mock=True)
await adapter.connect()
devices = await adapter.discover_devices()
```

## Troubleshooting

### Common Issues

#### No Devices Discovered
- Check network connectivity
- Verify API credentials
- Ensure provider service is running
- Check firewall rules

#### Commands Not Working
- Verify device is online in provider app
- Check device ID matches
- Review adapter logs for errors
- Try refreshing device cache

#### Connection Timeouts
- Increase timeout values in adapter config
- Check network latency
- Verify provider service health

### Debug Mode
Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Mock Device Database

For testing, the following mock devices are available:

### Lights
- Living Room Lights (light.living_room)
- Bedroom Lights (light.bedroom)
- Office Lights (light.office)
- Kitchen Lights (light.kitchen)

### Switches
- Porch Light (switch.porch_light)

### Smart Plugs
- Coffee Maker (plug.coffee_maker)
- Desk Lamp (plug.desk_lamp)

### Thermostats
- Main Thermostat (thermostat.main)

### Sensors
- Front Door Sensor (sensor.front_door)

### Locks
- Front Door Lock (lock.front_door)

### Scenes
- Movie Time
- Good Morning
- Good Night
- Work Mode
- Away Mode

## Future Enhancements

Potential additions:
- [ ] WebSocket support for real-time state updates
- [ ] Voice feedback for device states
- [ ] Automation rules engine
- [ ] Energy monitoring and reporting
- [ ] Multi-room audio control
- [ ] Camera integration
- [ ] Weather-based automations
- [ ] Geofencing support

## License

This integration is part of the Jarvis AI Assistant project.
