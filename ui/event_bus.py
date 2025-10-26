from PySide6.QtCore import QObject, Signal, Slot
from typing import Dict, Any, List
from datetime import datetime
import threading


class EventBus(QObject):
    conversation_updated = Signal(dict)
    task_updated = Signal(dict)
    system_metrics_updated = Signal(dict)
    memory_updated = Signal(dict)
    audio_data_updated = Signal(list)
    status_updated = Signal(str)
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
            return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            self._conversation_history: List[Dict[str, Any]] = []
            self._tasks: List[Dict[str, Any]] = []
            self._memory_items: List[Dict[str, Any]] = []
    
    @Slot(str, str)
    def add_conversation(self, speaker: str, message: str):
        entry = {
            'speaker': speaker,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self._conversation_history.append(entry)
        self.conversation_updated.emit(entry)
    
    @Slot(str, str, str)
    def add_task(self, task_id: str, description: str, status: str):
        task = {
            'id': task_id,
            'description': description,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        self._tasks.append(task)
        self.task_updated.emit(task)
    
    @Slot(dict)
    def update_metrics(self, metrics: Dict[str, Any]):
        self.system_metrics_updated.emit(metrics)
    
    @Slot(str, str)
    def add_memory(self, key: str, value: str):
        memory = {
            'key': key,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self._memory_items.append(memory)
        self.memory_updated.emit(memory)
    
    @Slot(list)
    def update_audio_waveform(self, data: List[float]):
        self.audio_data_updated.emit(data)
    
    @Slot(str)
    def update_status(self, status: str):
        self.status_updated.emit(status)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        return self._conversation_history
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        return self._tasks
    
    def get_memory_items(self) -> List[Dict[str, Any]]:
        return self._memory_items
