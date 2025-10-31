from typing import Dict, List, Any, Optional
import asyncio
from home_automation.base import (
    HomeAutomationAdapter, Device, DeviceType, DeviceState, Scene
)
from home_automation.mock_api import mock_db


class HomeAssistantAdapter(HomeAutomationAdapter):
    def __init__(self, config: Dict[str, Any], use_mock: bool = True):
        super().__init__(config)
        self.url = config.get('url', 'http://localhost:8123')
        self.token = config.get('token', '')
        self.websocket_url = config.get('websocket_url', 'ws://localhost:8123/api/websocket')
        self.use_mock = use_mock
        self.connected = False

    async def connect(self) -> bool:
        if self.use_mock:
            self.connected = True
            print(f"[HomeAssistant] Connected to mock Home Assistant at {self.url}")
            return True
        
        try:
            print(f"[HomeAssistant] Connecting to Home Assistant at {self.url}")
            self.connected = True
            return True
        except Exception as e:
            print(f"[HomeAssistant] Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        self.connected = False
        print("[HomeAssistant] Disconnected")

    async def discover_devices(self) -> List[Device]:
        if not self.connected:
            await self.connect()

        if self.use_mock:
            devices = mock_db.get_all_devices()
            self.cache_devices(devices)
            print(f"[HomeAssistant] Discovered {len(devices)} devices")
            return devices

        return []

    async def get_device_state(self, device_id: str) -> Optional[Device]:
        if self.use_mock:
            device = mock_db.get_device(device_id)
            if device:
                self._devices[device_id] = device
            return device
        
        return self.get_cached_device(device_id)

    async def set_device_state(self, device_id: str, state: DeviceState, **kwargs) -> bool:
        if self.use_mock:
            attributes = {}
            
            if 'brightness' in kwargs:
                attributes['brightness'] = kwargs['brightness']
            if 'color_temp' in kwargs:
                attributes['color_temp'] = kwargs['color_temp']
            if 'temperature' in kwargs:
                attributes['target_temperature'] = kwargs['temperature']
            if 'mode' in kwargs:
                attributes['mode'] = kwargs['mode']

            success = mock_db.update_device_state(device_id, state, attributes)
            if success:
                device = mock_db.get_device(device_id)
                if device:
                    self._devices[device_id] = device
                    print(f"[HomeAssistant] Updated {device_id} to {state.value}")
            return success

        return False

    async def get_scenes(self) -> List[Scene]:
        if not self.connected:
            await self.connect()

        if self.use_mock:
            scenes = mock_db.get_all_scenes()
            self.cache_scenes(scenes)
            print(f"[HomeAssistant] Discovered {len(scenes)} scenes")
            return scenes

        return []

    async def activate_scene(self, scene_id: str) -> bool:
        if self.use_mock:
            scene = mock_db.get_scene(scene_id)
            if scene:
                print(f"[HomeAssistant] Activating scene: {scene.name}")
                
                for device_id in scene.devices:
                    device = mock_db.get_device(device_id)
                    if device:
                        if device.device_type == DeviceType.LIGHT:
                            if "movie" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON, brightness=20)
                            elif "morning" in scene.name.lower() or "work" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON, brightness=100)
                            else:
                                await self.set_device_state(device_id, DeviceState.OFF)
                        elif device.device_type == DeviceType.PLUG:
                            if "morning" in scene.name.lower() or "work" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON)
                            else:
                                await self.set_device_state(device_id, DeviceState.OFF)
                        elif device.device_type == DeviceType.LOCK:
                            await self.set_device_state(device_id, DeviceState.ON)
                
                return True
        
        return False

    async def turn_on_light(self, device_id: str, brightness: Optional[int] = None) -> bool:
        kwargs = {}
        if brightness is not None:
            kwargs['brightness'] = brightness
        return await self.set_device_state(device_id, DeviceState.ON, **kwargs)

    async def turn_off_light(self, device_id: str) -> bool:
        return await self.set_device_state(device_id, DeviceState.OFF)

    async def dim_light(self, device_id: str, brightness: int) -> bool:
        return await self.set_device_state(device_id, DeviceState.ON, brightness=brightness)

    async def set_thermostat(self, device_id: str, temperature: float, mode: Optional[str] = None) -> bool:
        kwargs = {'temperature': temperature}
        if mode:
            kwargs['mode'] = mode
        return await self.set_device_state(device_id, DeviceState.ON, **kwargs)
