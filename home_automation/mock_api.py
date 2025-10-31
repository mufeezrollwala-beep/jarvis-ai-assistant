from typing import Dict, List, Any, Optional
from home_automation.base import Device, DeviceType, DeviceState, Scene
import random


class MockDeviceDatabase:
    def __init__(self):
        self.devices: Dict[str, Device] = self._create_mock_devices()
        self.scenes: Dict[str, Scene] = self._create_mock_scenes()

    def _create_mock_devices(self) -> Dict[str, Device]:
        devices = {
            "light.living_room": Device(
                device_id="light.living_room",
                name="Living Room Lights",
                device_type=DeviceType.LIGHT,
                state=DeviceState.OFF,
                attributes={"brightness": 0, "color_temp": 4000},
                room="Living Room"
            ),
            "light.bedroom": Device(
                device_id="light.bedroom",
                name="Bedroom Lights",
                device_type=DeviceType.LIGHT,
                state=DeviceState.OFF,
                attributes={"brightness": 0, "color_temp": 3000},
                room="Bedroom"
            ),
            "light.office": Device(
                device_id="light.office",
                name="Office Lights",
                device_type=DeviceType.LIGHT,
                state=DeviceState.ON,
                attributes={"brightness": 80, "color_temp": 5000},
                room="Office"
            ),
            "light.kitchen": Device(
                device_id="light.kitchen",
                name="Kitchen Lights",
                device_type=DeviceType.LIGHT,
                state=DeviceState.ON,
                attributes={"brightness": 100, "color_temp": 4500},
                room="Kitchen"
            ),
            "switch.porch_light": Device(
                device_id="switch.porch_light",
                name="Porch Light",
                device_type=DeviceType.SWITCH,
                state=DeviceState.OFF,
                room="Exterior"
            ),
            "plug.coffee_maker": Device(
                device_id="plug.coffee_maker",
                name="Coffee Maker",
                device_type=DeviceType.PLUG,
                state=DeviceState.OFF,
                attributes={"power": 0},
                room="Kitchen"
            ),
            "plug.desk_lamp": Device(
                device_id="plug.desk_lamp",
                name="Desk Lamp",
                device_type=DeviceType.PLUG,
                state=DeviceState.ON,
                attributes={"power": 12},
                room="Office"
            ),
            "thermostat.main": Device(
                device_id="thermostat.main",
                name="Main Thermostat",
                device_type=DeviceType.THERMOSTAT,
                state=DeviceState.ON,
                attributes={
                    "current_temperature": 22,
                    "target_temperature": 21,
                    "mode": "heat",
                    "humidity": 45
                },
                room="Living Room"
            ),
            "sensor.front_door": Device(
                device_id="sensor.front_door",
                name="Front Door Sensor",
                device_type=DeviceType.SENSOR,
                state=DeviceState.OFF,
                attributes={"battery": 85, "last_triggered": "2024-01-15T10:30:00"},
                room="Entrance"
            ),
            "lock.front_door": Device(
                device_id="lock.front_door",
                name="Front Door Lock",
                device_type=DeviceType.LOCK,
                state=DeviceState.ON,
                attributes={"locked": True},
                room="Entrance"
            )
        }
        return devices

    def _create_mock_scenes(self) -> Dict[str, Scene]:
        scenes = {
            "scene.movie_time": Scene(
                scene_id="scene.movie_time",
                name="Movie Time",
                description="Dim living room lights for movie watching",
                devices=["light.living_room"]
            ),
            "scene.good_morning": Scene(
                scene_id="scene.good_morning",
                name="Good Morning",
                description="Turn on bedroom and kitchen lights, start coffee maker",
                devices=["light.bedroom", "light.kitchen", "plug.coffee_maker"]
            ),
            "scene.good_night": Scene(
                scene_id="scene.good_night",
                name="Good Night",
                description="Turn off all lights and lock doors",
                devices=["light.living_room", "light.bedroom", "light.office", 
                        "light.kitchen", "lock.front_door"]
            ),
            "scene.work_mode": Scene(
                scene_id="scene.work_mode",
                name="Work Mode",
                description="Bright office lighting and optimal temperature",
                devices=["light.office", "thermostat.main", "plug.desk_lamp"]
            ),
            "scene.away": Scene(
                scene_id="scene.away",
                name="Away Mode",
                description="Turn off all devices and lock doors",
                devices=["light.living_room", "light.bedroom", "light.office", 
                        "light.kitchen", "plug.coffee_maker", "plug.desk_lamp",
                        "lock.front_door"]
            )
        }
        return scenes

    def get_device(self, device_id: str) -> Optional[Device]:
        return self.devices.get(device_id)

    def get_all_devices(self) -> List[Device]:
        return list(self.devices.values())

    def get_scene(self, scene_id: str) -> Optional[Scene]:
        return self.scenes.get(scene_id)

    def get_all_scenes(self) -> List[Scene]:
        return list(self.scenes.values())

    def update_device_state(self, device_id: str, state: DeviceState, attributes: Optional[Dict[str, Any]] = None) -> bool:
        device = self.devices.get(device_id)
        if device:
            device.update_state(state, attributes)
            return True
        return False

    def find_devices_by_type(self, device_type: DeviceType) -> List[Device]:
        return [d for d in self.devices.values() if d.device_type == device_type]

    def find_devices_by_room(self, room: str) -> List[Device]:
        return [d for d in self.devices.values() if d.room and d.room.lower() == room.lower()]

    def find_device_by_name(self, name: str) -> Optional[Device]:
        name_lower = name.lower()
        for device in self.devices.values():
            if device.name.lower() == name_lower or name_lower in device.name.lower():
                return device
        return None


mock_db = MockDeviceDatabase()
