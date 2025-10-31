from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class DeviceType(Enum):
    LIGHT = "light"
    SWITCH = "switch"
    THERMOSTAT = "thermostat"
    SENSOR = "sensor"
    PLUG = "plug"
    LOCK = "lock"
    CAMERA = "camera"
    UNKNOWN = "unknown"


class DeviceState(Enum):
    ON = "on"
    OFF = "off"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class Device:
    def __init__(
        self,
        device_id: str,
        name: str,
        device_type: DeviceType,
        state: DeviceState = DeviceState.UNKNOWN,
        attributes: Optional[Dict[str, Any]] = None,
        room: Optional[str] = None
    ):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.state = state
        self.attributes = attributes or {}
        self.room = room
        self.last_updated = datetime.now()

    def update_state(self, state: DeviceState, attributes: Optional[Dict[str, Any]] = None):
        self.state = state
        if attributes:
            self.attributes.update(attributes)
        self.last_updated = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'device_id': self.device_id,
            'name': self.name,
            'type': self.device_type.value,
            'state': self.state.value,
            'attributes': self.attributes,
            'room': self.room,
            'last_updated': self.last_updated.isoformat()
        }

    def __repr__(self) -> str:
        return f"Device({self.name}, {self.device_type.value}, {self.state.value})"


class Scene:
    def __init__(
        self,
        scene_id: str,
        name: str,
        description: Optional[str] = None,
        devices: Optional[List[str]] = None
    ):
        self.scene_id = scene_id
        self.name = name
        self.description = description
        self.devices = devices or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'scene_id': self.scene_id,
            'name': self.name,
            'description': self.description,
            'devices': self.devices
        }

    def __repr__(self) -> str:
        return f"Scene({self.name}, {len(self.devices)} devices)"


class HomeAutomationAdapter(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        self._devices: Dict[str, Device] = {}
        self._scenes: Dict[str, Scene] = {}

    @abstractmethod
    async def connect(self) -> bool:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def discover_devices(self) -> List[Device]:
        pass

    @abstractmethod
    async def get_device_state(self, device_id: str) -> Optional[Device]:
        pass

    @abstractmethod
    async def set_device_state(self, device_id: str, state: DeviceState, **kwargs) -> bool:
        pass

    @abstractmethod
    async def get_scenes(self) -> List[Scene]:
        pass

    @abstractmethod
    async def activate_scene(self, scene_id: str) -> bool:
        pass

    def get_cached_device(self, device_id: str) -> Optional[Device]:
        return self._devices.get(device_id)

    def get_cached_scene(self, scene_id: str) -> Optional[Scene]:
        return self._scenes.get(scene_id)

    def cache_devices(self, devices: List[Device]) -> None:
        for device in devices:
            self._devices[device.device_id] = device

    def cache_scenes(self, scenes: List[Scene]) -> None:
        for scene in scenes:
            self._scenes[scene.scene_id] = scene

    def list_devices(self) -> List[Device]:
        return list(self._devices.values())

    def list_scenes(self) -> List[Scene]:
        return list(self._scenes.values())
