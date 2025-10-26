# Jarvis Dashboard - System Architecture

## High-Level Overview

```
┌────────────────────────────────────────────────────────────────┐
│                     Jarvis AI Assistant                         │
│                      (jarvis.txt)                               │
└────────────────────┬───────────────────────────────────────────┘
                     │ Emits Events
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                       Event Bus                                 │
│                    (Singleton Pattern)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Qt Signals:                                              │  │
│  │ • conversation_updated                                   │  │
│  │ • task_updated                                          │  │
│  │ • system_metrics_updated                                │  │
│  │ • memory_updated                                        │  │
│  │ • audio_data_updated                                    │  │
│  │ • status_updated                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────┘
                     │ Qt Signal/Slot
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                   Dashboard Bridge                              │
│                   (QObject with Properties)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Properties exposed to QML:                               │  │
│  │ • conversation (list)                                    │  │
│  │ • tasks (list)                                          │  │
│  │ • metrics (dict)                                        │  │
│  │ • memory (list)                                         │  │
│  │ • audioData (list)                                      │  │
│  │ • status (string)                                       │  │
│  │ • highContrast (bool)                                   │  │
│  │ • fontScale (float)                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────┘
                     │ Property Binding
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                      QML Frontend                               │
│                    (Declarative UI)                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ main.qml (Main Layout)                                   │  │
│  │  ├─ Top Bar (Logo, Status, Accessibility Controls)       │  │
│  │  └─ Grid Layout (3x3)                                    │  │
│  │      ├─ ConversationPanel.qml (Left, Row 0-1)           │  │
│  │      ├─ TaskPanel.qml (Center, Row 0-1)                 │  │
│  │      ├─ MetricsPanel.qml (Right, Row 0)                 │  │
│  │      ├─ MemoryPanel.qml (Right, Row 1)                  │  │
│  │      └─ WaveformPanel.qml (Bottom, Row 2, Span 3)       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Python Backend

```
ui/
├── __init__.py
│   └── Exports: JarvisDashboard, DashboardBridge, EventBus, MockDataGenerator
│
├── event_bus.py
│   └── EventBus (Singleton)
│       ├── Qt Signals for each event type
│       ├── Slot methods for receiving events
│       └── History storage (bounded lists)
│
├── dashboard.py
│   ├── DashboardBridge (QObject)
│   │   ├── Qt Properties for data binding
│   │   ├── Qt Signals for property changes
│   │   ├── Slot methods for UI actions
│   │   └── Event bus connection
│   │
│   └── JarvisDashboard (Application)
│       ├── QGuiApplication initialization
│       ├── QQmlApplicationEngine setup
│       ├── Context property injection
│       └── Event loop management
│
└── mock_data.py
    └── MockDataGenerator (QThread)
        ├── Background thread for data generation
        ├── Realistic mock data patterns
        └── Configurable update intervals
```

### QML Frontend

```
ui/qml/
├── qmldir
│   └── Theme singleton registration
│
├── Theme.qml (Singleton)
│   ├── Color palette
│   ├── Typography settings
│   ├── Spacing/sizing constants
│   └── Animation durations
│
├── main.qml
│   ├── Window setup
│   ├── Background animations (grid, particles)
│   ├── Top bar (logo, status, controls)
│   └── GridLayout with 5 panels
│
├── ConversationPanel.qml
│   ├── ListView with chat messages
│   ├── Auto-scroll functionality
│   └── Fade-in animations
│
├── TaskPanel.qml
│   ├── ListView with tasks
│   ├── Status badges (pending/running/completed)
│   └── Slide-in animations
│
├── MetricsPanel.qml
│   ├── GridLayout (2x2)
│   ├── MetricItem component (inline)
│   └── Progress bars with animations
│
├── MemoryPanel.qml
│   ├── ListView with key-value pairs
│   ├── Timestamp display
│   └── Scale-in animations
│
└── WaveformPanel.qml
    ├── Canvas for custom rendering
    ├── Waveform drawing logic
    └── Live indicator animation
```

## Data Flow

### 1. Event Generation
```
Assistant Action → EventBus.add_conversation()
                → Signal emission
                → DashboardBridge slot
                → List append
                → Property change signal
                → QML list update
                → UI re-render
```

### 2. User Interaction
```
QML Button Click → Slot call on DashboardBridge
                 → Property change
                 → Property change signal
                 → QML binding update
                 → UI re-render
```

### 3. Mock Data Flow
```
MockDataGenerator (Thread) → Signal emission
                           → EventBus slot
                           → (Same as Event Generation)
```

### 4. System Metrics Flow
```
Timer tick → psutil.* calls
          → Metrics dict creation
          → EventBus.update_metrics()
          → (Same as Event Generation)
```

## Threading Model

```
┌─────────────────────────────────────────┐
│         Main Thread (UI)                │
│  ┌───────────────────────────────────┐  │
│  │ Qt Event Loop                     │  │
│  │  ├─ QML Rendering                 │  │
│  │  ├─ Event Processing              │  │
│  │  └─ Property Updates              │  │
│  └───────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  │ Qt Signal/Slot (Thread-Safe)
                  │
┌─────────────────┴───────────────────────┐
│      Background Threads                 │
│  ┌───────────────────────────────────┐  │
│  │ MockDataGenerator (QThread)       │  │
│  │  └─ Generates data every 2s       │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ Voice Assistant (Thread)          │  │
│  │  └─ Listens & processes commands  │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ Metrics Timer (QTimer)            │  │
│  │  └─ Updates system stats          │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Design Patterns

### 1. Singleton (EventBus)
- **Purpose**: Single point of event coordination
- **Implementation**: Python `__new__` override with thread lock
- **Benefits**: Global access, thread-safe initialization

### 2. Observer (Qt Signals/Slots)
- **Purpose**: Loose coupling between components
- **Implementation**: Qt's built-in signal/slot mechanism
- **Benefits**: Thread-safe, automatic connection management

### 3. Bridge (DashboardBridge)
- **Purpose**: Connect Python backend to QML frontend
- **Implementation**: QObject with Qt Properties
- **Benefits**: Type-safe data binding, automatic updates

### 4. Component (QML Components)
- **Purpose**: Reusable UI elements
- **Implementation**: QML inline components
- **Benefits**: Encapsulation, maintainability

### 5. MVVM (Overall Architecture)
- **Model**: EventBus, data storage
- **View**: QML components
- **ViewModel**: DashboardBridge
- **Benefits**: Separation of concerns, testability

## Communication Protocols

### Python → QML (Data Binding)
```python
@Property(list, notify=conversationChanged)
def conversation(self):
    return self._conversation_list
```
```qml
ListView {
    model: dashboard.conversation
    // Automatically updates when property changes
}
```

### QML → Python (Method Calls)
```qml
Button {
    onClicked: dashboard.toggleContrast()
}
```
```python
@Slot()
def toggleContrast(self):
    self.highContrast = not self._high_contrast
```

### Thread → Main Thread (Signals)
```python
# In background thread
self.conversation_signal.emit("User", "Hello")

# Received in main thread
event_bus.add_conversation("User", "Hello")
```

## State Management

### Centralized State (EventBus)
- Conversation history (list, max 50)
- Task list (list, max 20)
- Memory items (list, max 15)
- Current metrics (dict)
- Audio waveform (list, 50 points)

### UI State (DashboardBridge)
- High contrast mode (bool)
- Font scale (float, 0.5-2.0)
- Status message (string)

### Transient State (QML)
- Scroll positions
- Animation states
- Hover states
- Focus states

## Performance Considerations

### Memory Management
- **Bounded Lists**: Automatic pruning of old items
- **Lazy Loading**: QML delegates created on-demand
- **Object Pooling**: Qt's built-in object caching

### Rendering Optimization
- **Scene Graph**: Hardware-accelerated rendering
- **Culling**: Off-screen items not rendered
- **Batching**: Similar items rendered together
- **Caching**: Static content cached as textures

### Update Optimization
- **Rate Limiting**: Metrics update every 2 seconds
- **Debouncing**: Property changes batched
- **Partial Updates**: Only changed items re-rendered
- **Animation Throttling**: 60 FPS cap

## Error Handling

### Initialization Errors
```python
try:
    dashboard = JarvisDashboard()
    if not dashboard.initialize():
        # Handle initialization failure
        return 1
except Exception as e:
    # Handle critical errors
    print(f"Error: {e}")
    return 1
```

### Runtime Errors
- **Event Bus**: Try/except on signal emissions
- **Metrics**: Graceful fallback if psutil fails
- **QML**: Error messages logged to console
- **Threading**: Daemon threads prevent hangs

## Testing Strategy

### Unit Tests
- Event bus functionality
- Dashboard bridge properties
- Mock data generation

### Integration Tests
- UI launch (headless mode)
- Event flow (end-to-end)
- Property binding

### Manual Tests
- Visual inspection (all panels)
- Animation smoothness
- Accessibility features
- Performance monitoring

## Deployment

### Development Mode
```bash
python scripts/run_ui.py --mock
```
- Uses mock data
- Full animations
- All features enabled

### Production Mode
```bash
python scripts/run_ui.py
```
- Real system metrics
- Integrates with assistant
- Production event bus

### Testing Mode
```bash
python scripts/run_ui.py --headless
```
- Offscreen rendering
- No display required
- CI/CD compatible

## Security Considerations

### Input Validation
- All user inputs validated in Python
- QML property types enforced
- Bounded list sizes prevent DoS

### Resource Limits
- Maximum conversation history: 50
- Maximum task list: 20
- Maximum memory items: 15
- Update frequency caps

### Thread Safety
- Qt signal/slot mechanism used
- No shared mutable state
- EventBus singleton with locking

## Extensibility

### Adding New Panels
1. Create new QML file in `ui/qml/`
2. Add to `main.qml` GridLayout
3. Bind to dashboard properties
4. Add new EventBus signals if needed

### Adding New Themes
1. Modify `Theme.qml` colors
2. Add theme selector in UI
3. Store theme preference
4. Reload with new theme

### Adding New Metrics
1. Add to `update_metrics()` dict
2. Add to MetricsPanel.qml
3. Create new MetricItem instance

### Custom Visualizations
1. Create Canvas-based component
2. Implement onPaint handler
3. Connect to dashboard property
4. Request repaint on updates
