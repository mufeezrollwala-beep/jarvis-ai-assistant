from typing import Dict, List, Optional, Any
import asyncio
from home_automation.base import (
    HomeAutomationAdapter, Device, DeviceType, DeviceState, Scene
)
from home_automation.adapters import HomeAssistantAdapter, HueAdapter, TPLinkAdapter
from home_automation.config import ConfigManager, MockConfigManager


class HomeAutomationService:
    def __init__(self, config_manager: Optional[ConfigManager] = None, use_mock: bool = True):
        self.config_manager = config_manager or MockConfigManager()
        self.use_mock = use_mock
        self.adapters: Dict[str, HomeAutomationAdapter] = {}
        self._all_devices: Dict[str, Device] = {}
        self._all_scenes: Dict[str, Scene] = {}
        self._device_to_adapter: Dict[str, str] = {}

    async def initialize(self):
        await self._load_adapters()
        await self.discover_all_devices()

    async def _load_adapters(self):
        providers = self.config_manager.list_providers()
        
        for provider in providers:
            config = self.config_manager.get_provider_config(provider)
            
            if provider == 'home_assistant':
                adapter = HomeAssistantAdapter(config, use_mock=self.use_mock)
                self.adapters['home_assistant'] = adapter
                await adapter.connect()
            
            elif provider == 'hue':
                adapter = HueAdapter(config, use_mock=self.use_mock)
                self.adapters['hue'] = adapter
                await adapter.connect()
            
            elif provider == 'tplink':
                adapter = TPLinkAdapter(config, use_mock=self.use_mock)
                self.adapters['tplink'] = adapter
                await adapter.connect()

    def register_adapter(self, name: str, adapter: HomeAutomationAdapter):
        self.adapters[name] = adapter
        print(f"[Service] Registered adapter: {name}")

    async def discover_all_devices(self):
        self._all_devices.clear()
        self._device_to_adapter.clear()
        
        for adapter_name, adapter in self.adapters.items():
            devices = await adapter.discover_devices()
            for device in devices:
                self._all_devices[device.device_id] = device
                self._device_to_adapter[device.device_id] = adapter_name
        
        print(f"[Service] Total devices discovered: {len(self._all_devices)}")
        
        for adapter_name, adapter in self.adapters.items():
            scenes = await adapter.get_scenes()
            for scene in scenes:
                self._all_scenes[scene.scene_id] = scene

    def list_devices(self, device_type: Optional[DeviceType] = None, room: Optional[str] = None) -> List[Device]:
        devices = list(self._all_devices.values())
        
        if device_type:
            devices = [d for d in devices if d.device_type == device_type]
        
        if room:
            devices = [d for d in devices if d.room and d.room.lower() == room.lower()]
        
        return devices

    def list_scenes(self) -> List[Scene]:
        return list(self._all_scenes.values())

    def get_device(self, device_id: str) -> Optional[Device]:
        return self._all_devices.get(device_id)

    def find_device_by_name(self, name: str) -> Optional[Device]:
        name_lower = name.lower()
        for device in self._all_devices.values():
            if device.name.lower() == name_lower or name_lower in device.name.lower():
                return device
        return None

    def find_scene_by_name(self, name: str) -> Optional[Scene]:
        name_lower = name.lower()
        for scene in self._all_scenes.values():
            if scene.name.lower() == name_lower or name_lower in scene.name.lower():
                return scene
        return None

    async def get_device_state(self, device_id: str) -> Optional[Device]:
        adapter_name = self._device_to_adapter.get(device_id)
        if adapter_name and adapter_name in self.adapters:
            adapter = self.adapters[adapter_name]
            device = await adapter.get_device_state(device_id)
            if device:
                self._all_devices[device_id] = device
            return device
        return None

    async def set_device_state(self, device_id: str, state: DeviceState, **kwargs) -> bool:
        adapter_name = self._device_to_adapter.get(device_id)
        if adapter_name and adapter_name in self.adapters:
            adapter = self.adapters[adapter_name]
            success = await adapter.set_device_state(device_id, state, **kwargs)
            if success:
                await self.get_device_state(device_id)
            return success
        return False

    async def turn_on_device(self, device_identifier: str, **kwargs) -> bool:
        device = self.get_device(device_identifier)
        if not device:
            device = self.find_device_by_name(device_identifier)
        
        if device:
            return await self.set_device_state(device.device_id, DeviceState.ON, **kwargs)
        return False

    async def turn_off_device(self, device_identifier: str) -> bool:
        device = self.get_device(device_identifier)
        if not device:
            device = self.find_device_by_name(device_identifier)
        
        if device:
            return await self.set_device_state(device.device_id, DeviceState.OFF)
        return False

    async def dim_light(self, light_identifier: str, brightness: int) -> bool:
        device = self.get_device(light_identifier)
        if not device:
            device = self.find_device_by_name(light_identifier)
        
        if device and device.device_type == DeviceType.LIGHT:
            return await self.set_device_state(device.device_id, DeviceState.ON, brightness=brightness)
        return False

    async def set_thermostat_temperature(self, thermostat_identifier: str, temperature: float) -> bool:
        device = self.get_device(thermostat_identifier)
        if not device:
            device = self.find_device_by_name(thermostat_identifier)
        
        if device and device.device_type == DeviceType.THERMOSTAT:
            return await self.set_device_state(device.device_id, DeviceState.ON, temperature=temperature)
        return False

    async def activate_scene(self, scene_identifier: str) -> bool:
        scene = self._all_scenes.get(scene_identifier)
        if not scene:
            scene = self.find_scene_by_name(scene_identifier)
        
        if scene:
            for adapter in self.adapters.values():
                if await adapter.activate_scene(scene.scene_id):
                    return True
        return False

    async def turn_off_room(self, room: str) -> bool:
        devices = self.list_devices(room=room)
        success = True
        for device in devices:
            if device.device_type in [DeviceType.LIGHT, DeviceType.SWITCH, DeviceType.PLUG]:
                result = await self.turn_off_device(device.device_id)
                success = success and result
        return success

    async def turn_on_room(self, room: str) -> bool:
        devices = self.list_devices(room=room)
        success = True
        for device in devices:
            if device.device_type in [DeviceType.LIGHT, DeviceType.SWITCH, DeviceType.PLUG]:
                result = await self.turn_on_device(device.device_id)
                success = success and result
        return success

    def get_device_summary(self) -> str:
        summary_lines = ["Home Automation Device Summary:", ""]
        
        by_type: Dict[DeviceType, List[Device]] = {}
        for device in self._all_devices.values():
            if device.device_type not in by_type:
                by_type[device.device_type] = []
            by_type[device.device_type].append(device)
        
        for device_type, devices in sorted(by_type.items(), key=lambda x: x[0].value):
            summary_lines.append(f"{device_type.value.upper()}S ({len(devices)}):")
            for device in sorted(devices, key=lambda d: d.name):
                state_str = f"{device.state.value}"
                if device.device_type == DeviceType.LIGHT and device.state == DeviceState.ON:
                    brightness = device.attributes.get('brightness', 'N/A')
                    state_str = f"{device.state.value} (brightness: {brightness})"
                elif device.device_type == DeviceType.THERMOSTAT:
                    temp = device.attributes.get('current_temperature', 'N/A')
                    target = device.attributes.get('target_temperature', 'N/A')
                    state_str = f"{temp}°C → {target}°C"
                summary_lines.append(f"  - {device.name} [{device.room or 'Unknown'}]: {state_str}")
            summary_lines.append("")
        
        if self._all_scenes:
            summary_lines.append(f"SCENES ({len(self._all_scenes)}):")
            for scene in sorted(self._all_scenes.values(), key=lambda s: s.name):
                summary_lines.append(f"  - {scene.name}: {scene.description or 'No description'}")
        
        return "\n".join(summary_lines)

    async def shutdown(self):
        for adapter in self.adapters.values():
            await adapter.disconnect()
