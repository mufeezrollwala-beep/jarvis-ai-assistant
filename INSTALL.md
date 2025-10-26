# Installation Guide - Jarvis Dashboard

## System Requirements

- **Python**: 3.9 or higher
- **Operating System**: Linux (tested), Windows/macOS (should work)
- **RAM**: 2 GB minimum, 4 GB recommended
- **Display**: 1280x720 minimum, 1600x900 recommended

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies (Linux)

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    libgl1 \
    libegl1 \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-cursor0 \
    libdbus-1-3
```

For Fedora/RHEL:
```bash
sudo dnf install -y \
    mesa-libGL \
    mesa-libEGL \
    glib2 \
    libxkbcommon-x11 \
    libxcb \
    dbus-libs
```

### 5. Launch Dashboard
```bash
# With mock data (recommended for first run)
python scripts/run_ui.py --mock

# With real system metrics
python scripts/run_ui.py
```

## Verification

Test the installation:
```bash
python scripts/test_ui.py
```

Expected output:
```
======================================================================
  J.A.R.V.I.S Dashboard - Unit Tests
======================================================================

Testing UI module imports...
✓ All imports successful!

Testing Event Bus...
  - Conversation history: 2
  - Tasks: 1
  - Memory items: 1
✓ Event Bus test passed!

======================================================================
  All tests passed!
======================================================================
```

## Troubleshooting

### Qt Platform Plugin Error
**Error**: `qt.qpa.plugin: Could not load the Qt platform plugin`

**Solution**: Install Qt platform dependencies (see System Dependencies above)

### Import Error: PySide6
**Error**: `ModuleNotFoundError: No module named 'PySide6'`

**Solution**: 
```bash
source .venv/bin/activate
pip install PySide6 psutil
```

### OpenGL/EGL Errors
**Error**: `libGL.so.1: cannot open shared object file`

**Solution**: Install OpenGL libraries
```bash
sudo apt-get install -y libgl1 libegl1
```

### Permission Denied
**Error**: `Permission denied: scripts/run_ui.py`

**Solution**: Make scripts executable
```bash
chmod +x scripts/run_ui.py
```

### Display Issues in Headless Environment
**Solution**: Use headless mode
```bash
python scripts/run_ui.py --mock --headless
```

## Configuration

### Audio Device (for voice assistant)
If you encounter audio device errors, install:
```bash
# Linux
sudo apt-get install -y portaudio19-dev python3-pyaudio

# macOS
brew install portaudio
```

### Weather API (optional)
To enable weather features:
1. Get API key from https://openweathermap.org/api
2. Edit `jarvis.txt` line 74
3. Replace `YOUR_WEATHER_API_KEY` with your key

### WolframAlpha API (optional)
To enable WolframAlpha features:
1. Get API key from https://products.wolframalpha.com/api/
2. Update your integration code

## Development Setup

### Running in Development Mode
```bash
# Mock data for UI development
python scripts/run_ui.py --mock

# Real metrics but no voice assistant
python scripts/run_ui.py
```

### Integration Testing
```bash
# Integrated mode (UI + Assistant placeholder)
python scripts/run_integrated.py
```

### Headless Testing
```bash
# For CI/CD environments
python scripts/run_ui.py --mock --headless
```

## Docker (Optional)

### Build Image
```bash
docker build -t jarvis-dashboard .
```

### Run Container
```bash
docker run -it \
    --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    jarvis-dashboard \
    python scripts/run_ui.py --mock
```

## Next Steps

1. **Explore the UI**: Launch with `--mock` flag to see all features
2. **Read Documentation**: Check `DASHBOARD_FEATURES.md` for complete feature list
3. **Integration**: See `ui/README.md` for integration API
4. **Customize**: Modify `ui/qml/Theme.qml` for color schemes

## Support

For issues, please:
1. Check this guide's Troubleshooting section
2. Review error messages carefully
3. Verify all dependencies are installed
4. Test with `--headless` mode if display issues occur

## Uninstallation

```bash
# Remove virtual environment
rm -rf .venv

# Remove installed files
rm -rf ui/__pycache__
rm -rf scripts/__pycache__
```
