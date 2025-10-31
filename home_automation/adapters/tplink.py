from typing import Dict, List, Any, Optional
import asyncio
from home_automation.base import (
    HomeAutomationAdapter, Device, DeviceType, DeviceState, Scene
)
from home_automation.mock_api import mock_db


class TPLinkAdapter(HomeAutomationAdapter):
    def __init__(self, config: Dict[str, Any], use_mock: bool = True):
        super().__init__(config)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.use_mock = use_mock
        self.connected = False

    async def connect(self) -> bool:
        if self.use_mock:
            self.connected = True
            print(f"[TPLink] Connected to mock TP-Link cloud")
            return True
        
        try:
            print(f"[TPLink] Connecting to TP-Link cloud")
            self.connected = True
            return True
        except Exception as e:
            print(f"[TPLink] Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        self.connected = False
        print("[TPLink] Disconnected")

    async def discover_devices(self) -> List[Device]:
        if not self.connected:
            await self.connect()

        if self.use_mock:
            plugs = mock_db.find_devices_by_type(DeviceType.PLUG)
            switches = mock_db.find_devices_by_type(DeviceType.SWITCH)
            devices = plugs + switches
            self.cache_devices(devices)
            print(f"[TPLink] Discovered {len(devices)} TP-Link devices")
            return devices

        return []

    async def get_device_state(self, device_id: str) -> Optional[Device]:
        if self.use_mock:
            device = mock_db.get_device(device_id)
            if device and device.device_type in [DeviceType.PLUG, DeviceType.SWITCH]:
                self._devices[device_id] = device
                return device
        
        return self.get_cached_device(device_id)

    async def set_device_state(self, device_id: str, state: DeviceState, **kwargs) -> bool:
        if self.use_mock:
            device = mock_db.get_device(device_id)
            if device and device.device_type in [DeviceType.PLUG, DeviceType.SWITCH]:
                attributes = {}
                
                if state == DeviceState.ON and device.device_type == DeviceType.PLUG:
                    attributes['power'] = kwargs.get('power', 12)
                elif state == DeviceState.OFF and device.device_type == DeviceType.PLUG:
                    attributes['power'] = 0

                success = mock_db.update_device_state(device_id, state, attributes)
                if success:
                    device = mock_db.get_device(device_id)
                    self._devices[device_id] = device
                    print(f"[TPLink] Updated {device_id} to {state.value}")
                return success

        return False

    async def get_scenes(self) -> List[Scene]:
        return []

    async def activate_scene(self, scene_id: str) -> bool:
        return False

    async def get_power_consumption(self, device_id: str) -> Optional[float]:
        if self.use_mock:
            device = mock_db.get_device(device_id)
            if device and device.device_type == DeviceType.PLUG:
                return device.attributes.get('power', 0)
        
        return None

    async def turn_on(self, device_id: str) -> bool:
        return await self.set_device_state(device_id, DeviceState.ON)

    async def turn_off(self, device_id: str) -> bool:
        return await self.set_device_state(device_id, DeviceState.OFF)
