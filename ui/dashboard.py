import sys
import os
import time
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer
from typing import List, Dict, Any
import psutil
from datetime import datetime

from ui.event_bus import EventBus
from ui.mock_data import MockDataGenerator


class DashboardBridge(QObject):
    conversationChanged = Signal()
    tasksChanged = Signal()
    metricsChanged = Signal()
    memoryChanged = Signal()
    audioDataChanged = Signal()
    statusChanged = Signal()
    themeChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self._event_bus = EventBus()
        self._conversation_list: List[Dict[str, str]] = []
        self._task_list: List[Dict[str, str]] = []
        self._metrics: Dict[str, float] = {}
        self._memory_list: List[Dict[str, str]] = []
        self._audio_data: List[float] = []
        self._status: str = "Initializing..."
        self._high_contrast: bool = False
        self._font_scale: float = 1.0
        
        self._mock_generator = None
        self._metrics_timer = QTimer()
        self._metrics_timer.timeout.connect(self._update_real_metrics)
        
        self._event_bus.conversation_updated.connect(self._on_conversation_updated)
        self._event_bus.task_updated.connect(self._on_task_updated)
        self._event_bus.system_metrics_updated.connect(self._on_metrics_updated)
        self._event_bus.memory_updated.connect(self._on_memory_updated)
        self._event_bus.audio_data_updated.connect(self._on_audio_updated)
        self._event_bus.status_updated.connect(self._on_status_updated)
    
    @Property(list, notify=conversationChanged)
    def conversation(self):
        return self._conversation_list
    
    @Property(list, notify=tasksChanged)
    def tasks(self):
        return self._task_list
    
    @Property('QVariantMap', notify=metricsChanged)
    def metrics(self):
        return self._metrics
    
    @Property(list, notify=memoryChanged)
    def memory(self):
        return self._memory_list
    
    @Property(list, notify=audioDataChanged)
    def audioData(self):
        return self._audio_data
    
    @Property(str, notify=statusChanged)
    def status(self):
        return self._status
    
    @Property(bool, notify=themeChanged)
    def highContrast(self):
        return self._high_contrast
    
    @highContrast.setter
    def highContrast(self, value: bool):
        if self._high_contrast != value:
            self._high_contrast = value
            self.themeChanged.emit()
    
    @Property(float, notify=themeChanged)
    def fontScale(self):
        return self._font_scale
    
    @fontScale.setter
    def fontScale(self, value: float):
        if self._font_scale != value:
            self._font_scale = max(0.5, min(2.0, value))
            self.themeChanged.emit()
    
    @Slot()
    def startMockMode(self):
        if self._mock_generator is None or not self._mock_generator.isRunning():
            self._mock_generator = MockDataGenerator()
            self._mock_generator.conversation_signal.connect(self._event_bus.add_conversation)
            self._mock_generator.task_signal.connect(self._event_bus.add_task)
            self._mock_generator.metrics_signal.connect(self._event_bus.update_metrics)
            self._mock_generator.memory_signal.connect(self._event_bus.add_memory)
            self._mock_generator.audio_signal.connect(self._event_bus.update_audio_waveform)
            self._mock_generator.status_signal.connect(self._event_bus.update_status)
            self._mock_generator.start()
            self._status = "Mock mode active"
            self.statusChanged.emit()
    
    @Slot()
    def stopMockMode(self):
        if self._mock_generator and self._mock_generator.isRunning():
            self._mock_generator.stop()
            self._mock_generator.wait()
            self._status = "Mock mode stopped"
            self.statusChanged.emit()
    
    @Slot()
    def startRealMode(self):
        self._metrics_timer.start(2000)
        self._status = "Real-time mode active"
        self.statusChanged.emit()
    
    @Slot()
    def stopRealMode(self):
        self._metrics_timer.stop()
        self._status = "Real-time mode stopped"
        self.statusChanged.emit()
    
    @Slot()
    def toggleContrast(self):
        self.highContrast = not self._high_contrast
    
    @Slot(float)
    def setFontScale(self, scale: float):
        self.fontScale = scale
    
    @Slot()
    def clearConversation(self):
        self._conversation_list.clear()
        self.conversationChanged.emit()
    
    @Slot()
    def clearTasks(self):
        self._task_list.clear()
        self.tasksChanged.emit()
    
    def _on_conversation_updated(self, entry: Dict[str, str]):
        self._conversation_list.append(entry)
        if len(self._conversation_list) > 50:
            self._conversation_list.pop(0)
        self.conversationChanged.emit()
    
    def _on_task_updated(self, task: Dict[str, str]):
        self._task_list.append(task)
        if len(self._task_list) > 20:
            self._task_list.pop(0)
        self.tasksChanged.emit()
    
    def _on_metrics_updated(self, metrics: Dict[str, Any]):
        self._metrics = metrics
        self.metricsChanged.emit()
    
    def _on_memory_updated(self, memory: Dict[str, str]):
        self._memory_list.append(memory)
        if len(self._memory_list) > 15:
            self._memory_list.pop(0)
        self.memoryChanged.emit()
    
    def _on_audio_updated(self, data: List[float]):
        self._audio_data = data
        self.audioDataChanged.emit()
    
    def _on_status_updated(self, status: str):
        self._status = status
        self.statusChanged.emit()
    
    def _update_real_metrics(self):
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net_io = psutil.net_io_counters()
            
            metrics = {
                'cpu': cpu,
                'memory': memory,
                'disk': disk,
                'network_in': net_io.bytes_recv / 1024 / 1024,
                'network_out': net_io.bytes_sent / 1024 / 1024,
                'uptime': time.time() - psutil.boot_time(),
            }
            
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    metrics['temperature'] = list(temps.values())[0][0].current
            except:
                pass
            
            self._event_bus.update_metrics(metrics)
        except Exception as e:
            print(f"Error updating metrics: {e}")


class JarvisDashboard:
    def __init__(self, mock_mode: bool = False, headless_safe: bool = False):
        self.app = None
        self.engine = None
        self.bridge = None
        self.mock_mode = mock_mode
        self.headless_safe = headless_safe
    
    def initialize(self) -> bool:
        try:
            if self.headless_safe:
                os.environ['QT_QPA_PLATFORM'] = 'offscreen'
            
            self.app = QGuiApplication(sys.argv)
            self.app.setOrganizationName("Jarvis")
            self.app.setOrganizationDomain("jarvis.ai")
            self.app.setApplicationName("Jarvis Dashboard")
            
            self.engine = QQmlApplicationEngine()
            self.bridge = DashboardBridge()
            
            self.engine.rootContext().setContextProperty("dashboard", self.bridge)
            
            qml_file = Path(__file__).parent / "qml" / "main.qml"
            self.engine.load(qml_file)
            
            if not self.engine.rootObjects():
                print("Failed to load QML file")
                return False
            
            if self.mock_mode:
                self.bridge.startMockMode()
            else:
                self.bridge.startRealMode()
            
            return True
            
        except Exception as e:
            print(f"Error initializing dashboard: {e}")
            if not self.headless_safe:
                raise
            return False
    
    def run(self) -> int:
        if not self.initialize():
            return 1
        
        try:
            return self.app.exec()
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            return 0
        finally:
            if self.bridge:
                self.bridge.stopMockMode()
                self.bridge.stopRealMode()
    
    def get_bridge(self) -> DashboardBridge:
        return self.bridge
