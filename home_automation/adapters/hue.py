from typing import Dict, List, Any, Optional
import asyncio
from home_automation.base import (
    HomeAutomationAdapter, Device, DeviceType, DeviceState, Scene
)
from home_automation.mock_api import mock_db


class HueAdapter(HomeAutomationAdapter):
    def __init__(self, config: Dict[str, Any], use_mock: bool = True):
        super().__init__(config)
        self.bridge_ip = config.get('bridge_ip', '192.168.1.100')
        self.username = config.get('username', '')
        self.api_key = config.get('api_key', '')
        self.use_mock = use_mock
        self.connected = False

    async def connect(self) -> bool:
        if self.use_mock:
            self.connected = True
            print(f"[Hue] Connected to mock Hue Bridge at {self.bridge_ip}")
            return True
        
        try:
            print(f"[Hue] Connecting to Hue Bridge at {self.bridge_ip}")
            self.connected = True
            return True
        except Exception as e:
            print(f"[Hue] Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        self.connected = False
        print("[Hue] Disconnected")

    async def discover_devices(self) -> List[Device]:
        if not self.connected:
            await self.connect()

        if self.use_mock:
            all_devices = mock_db.find_devices_by_type(DeviceType.LIGHT)
            hue_devices = [d for d in all_devices if 'hue' not in d.device_id]
            self.cache_devices(hue_devices)
            print(f"[Hue] Discovered {len(hue_devices)} Hue lights")
            return hue_devices

        return []

    async def get_device_state(self, device_id: str) -> Optional[Device]:
        if self.use_mock:
            device = mock_db.get_device(device_id)
            if device and device.device_type == DeviceType.LIGHT:
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
            if 'hue' in kwargs:
                attributes['hue'] = kwargs['hue']
            if 'saturation' in kwargs:
                attributes['saturation'] = kwargs['saturation']

            device = mock_db.get_device(device_id)
            if device and device.device_type == DeviceType.LIGHT:
                success = mock_db.update_device_state(device_id, state, attributes)
                if success:
                    device = mock_db.get_device(device_id)
                    self._devices[device_id] = device
                    print(f"[Hue] Updated {device_id} to {state.value}")
                return success

        return False

    async def get_scenes(self) -> List[Scene]:
        if not self.connected:
            await self.connect()

        if self.use_mock:
            all_scenes = mock_db.get_all_scenes()
            hue_scenes = [s for s in all_scenes if any(
                d.startswith('light.') for d in s.devices
            )]
            self.cache_scenes(hue_scenes)
            print(f"[Hue] Discovered {len(hue_scenes)} Hue scenes")
            return hue_scenes

        return []

    async def activate_scene(self, scene_id: str) -> bool:
        if self.use_mock:
            scene = mock_db.get_scene(scene_id)
            if scene:
                print(f"[Hue] Activating scene: {scene.name}")
                
                for device_id in scene.devices:
                    if device_id.startswith('light.'):
                        device = mock_db.get_device(device_id)
                        if device:
                            if "movie" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON, brightness=15, color_temp=2700)
                            elif "morning" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON, brightness=100, color_temp=5000)
                            elif "work" in scene.name.lower():
                                await self.set_device_state(device_id, DeviceState.ON, brightness=90, color_temp=4500)
                            else:
                                await self.set_device_state(device_id, DeviceState.OFF)
                
                return True
        
        return False

    async def set_color(self, device_id: str, hue: int, saturation: int, brightness: Optional[int] = None) -> bool:
        kwargs = {'hue': hue, 'saturation': saturation}
        if brightness is not None:
            kwargs['brightness'] = brightness
        return await self.set_device_state(device_id, DeviceState.ON, **kwargs)

    async def set_color_temperature(self, device_id: str, color_temp: int) -> bool:
        return await self.set_device_state(device_id, DeviceState.ON, color_temp=color_temp)
