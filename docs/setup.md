# Setup Guide

This comprehensive guide will walk you through setting up JARVIS on your system, regardless of your operating system or experience level.

## Table of Contents

- [System Requirements](#system-requirements)
- [Python Installation](#python-installation)
- [Project Setup](#project-setup)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Dependency Installation](#dependency-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, Debian 10+)
- **Python**: Version 3.8 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Storage**: 500 MB free space for dependencies
- **Audio**: Microphone input and speaker/headphone output
- **Network**: Internet connection for cloud services

### Recommended Hardware

- **Microphone**: USB or built-in microphone with noise cancellation
- **Processor**: Multi-core CPU for better performance
- **Audio Interface**: Good quality audio output for clear TTS

## Python Installation

### Checking Existing Python Installation

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run:

```bash
python --version
```

or

```bash
python3 --version
```

If you see Python 3.8 or higher, you're good to go! If not, follow the instructions below.

### Installing Python

#### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

#### macOS

**Option 1: Official Installer**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the `.pkg` installer
3. Follow installation prompts

**Option 2: Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.12
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install python3 python3-pip
```

## Project Setup

### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/yourusername/jarvis-ai-assistant.git

# Using SSH (if configured)
git clone git@github.com:yourusername/jarvis-ai-assistant.git

# Navigate into directory
cd jarvis-ai-assistant
```

### 2. Create Virtual Environment

A virtual environment keeps JARVIS dependencies isolated from your system Python.

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> **Note**: Your terminal prompt should now show `(.venv)` indicating the virtual environment is active.

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Platform-Specific Instructions

### Windows Setup

#### Install PyAudio

PyAudio is required for microphone access but can be tricky on Windows.

**Method 1: pip (Try this first)**
```cmd
pip install pyaudio
```

**Method 2: Pre-compiled Wheel (if Method 1 fails)**
1. Visit [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Download the appropriate `.whl` file for your Python version
   - For Python 3.12, 64-bit: `PyAudio‑0.2.14‑cp312‑cp312‑win_amd64.whl`
3. Install it:
   ```cmd
   pip install path\to\downloaded\PyAudio‑0.2.14‑cp312‑cp312‑win_amd64.whl
   ```

#### Configure Audio Permissions

1. Open Settings → Privacy → Microphone
2. Enable "Allow apps to access your microphone"
3. Enable for Python or your terminal application

### macOS Setup

#### Install System Dependencies

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PortAudio (required for PyAudio)
brew install portaudio

# Install PyAudio
pip install pyaudio
```

#### Grant Microphone Permissions

1. Go to System Preferences → Security & Privacy → Privacy
2. Select "Microphone" in the left sidebar
3. Check the box next to Terminal or your Python IDE

### Linux Setup

#### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-pyaudio \
    portaudio19-dev \
    python3-dev \
    libasound2-dev \
    espeak

# Install Python packages
pip install pyaudio
```

#### Fedora/RHEL

```bash
# Install system dependencies
sudo dnf install -y \
    portaudio-devel \
    python3-devel \
    alsa-lib-devel \
    espeak

# Install Python packages
pip install pyaudio
```

#### Arch Linux

```bash
# Install system dependencies
sudo pacman -S portaudio espeak python-pyaudio

# Install Python packages
pip install pyaudio
```

## Dependency Installation

### Install All Python Dependencies

Create a `requirements.txt` file in the project root (if not present):

```txt
speechrecognition>=3.10.0
pyttsx3>=2.90
wikipedia>=1.4.0
requests>=2.31.0
wolframalpha>=5.0.0
pyaudio>=0.2.13
```

Then install:

```bash
pip install -r requirements.txt
```

### Individual Package Installation

If you prefer to install packages individually:

```bash
pip install speechrecognition
pip install pyttsx3
pip install wikipedia
pip install requests
pip install wolframalpha
pip install pyaudio
```

## Verification

### Test Audio Input

Run this script to test microphone access:

```python
import speech_recognition as sr

# List available microphones
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

# Test recording
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("\nAdjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("Say something!")
    audio = recognizer.listen(source, timeout=5)
    print("Audio captured successfully!")
```

Save as `test_microphone.py` and run:
```bash
python test_microphone.py
```

### Test Text-to-Speech

```python
import pyttsx3

engine = pyttsx3.init()
engine.say("Hello, I am Jarvis. Audio output is working correctly.")
engine.runAndWait()
print("If you heard the voice, TTS is working!")
```

Save as `test_tts.py` and run:
```bash
python test_tts.py
```

### Test Speech Recognition

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    print("Say something (you have 5 seconds):")
    
    try:
        audio = recognizer.listen(source, timeout=5)
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.WaitTimeoutError:
        print("No speech detected")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Recognition error: {e}")
```

Save as `test_recognition.py` and run:
```bash
python test_recognition.py
```

### Run JARVIS

If all tests pass, you're ready to run JARVIS:

```bash
python jarvis.txt
```

You should hear a greeting based on the time of day!

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError: No module named 'X'"

**Solution:**
```bash
# Ensure virtual environment is activated
# Then install the missing module
pip install module-name
```

#### Issue: "PyAudio could not find PortAudio"

**Windows Solution:**
- Download and install the PyAudio wheel as described in [Windows Setup](#windows-setup)

**macOS Solution:**
```bash
brew install portaudio
pip uninstall pyaudio
pip install --no-cache-dir pyaudio
```

**Linux Solution:**
```bash
sudo apt-get install portaudio19-dev
pip install --no-cache-dir pyaudio
```

#### Issue: "No microphone detected" or "list index out of range"

**Solutions:**

1. **Check microphone connection**
   - Ensure microphone is plugged in
   - Try a different USB port
   - Test in another application (Zoom, Discord, etc.)

2. **List available devices**
   ```python
   import speech_recognition as sr
   print(sr.Microphone.list_microphone_names())
   ```

3. **Specify microphone index**
   ```python
   # If your microphone is at index 2
   with sr.Microphone(device_index=2) as source:
       # your code
   ```

#### Issue: "Speech recognition not working" or "UnknownValueError"

**Solutions:**

1. **Check internet connection** (Google Speech Recognition requires internet)
2. **Adjust energy threshold**
   ```python
   recognizer.energy_threshold = 4000  # Increase for noisy environments
   ```
3. **Increase pause threshold**
   ```python
   recognizer.pause_threshold = 1.5  # Wait longer before processing
   ```
4. **Speak clearly** and ensure minimal background noise

#### Issue: "Text-to-speech not working" or "No audio output"

**Windows:**
- Ensure SAPI5 voices are installed
- Check: Control Panel → Speech Recognition → Text to Speech

**macOS:**
- Check System Preferences → Accessibility → Speech
- Install additional voices if needed

**Linux:**
```bash
# Install espeak
sudo apt-get install espeak

# Or install festival
sudo apt-get install festival
```

#### Issue: "Permission denied" errors

**Solutions:**

1. **Don't run as administrator/root** (security risk)
2. **Grant microphone permissions** (see platform-specific sections)
3. **Check file permissions**
   ```bash
   chmod +x jarvis.txt
   ```

#### Issue: "API calls failing" (Weather, Wikipedia, etc.)

**Solutions:**

1. **Check internet connection**
2. **Verify API keys** are correctly configured
3. **Check API rate limits** (you may have exceeded free tier)
4. **Firewall settings** - ensure Python can make outbound connections

#### Issue: "High CPU usage"

**Solutions:**

1. **Adjust recognition settings**
   ```python
   recognizer.pause_threshold = 0.8  # Reduce for faster processing
   recognizer.energy_threshold = 300  # Lower for quieter environments
   ```

2. **Use specific microphone** instead of default
3. **Close other audio applications**

### Getting Help

If you're still experiencing issues:

1. **Check documentation**: Review all docs in the `docs/` directory
2. **Search existing issues**: [GitHub Issues](https://github.com/yourusername/jarvis-ai-assistant/issues)
3. **Enable debug logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
4. **Create an issue**: Include your OS, Python version, and error messages

### Debug Mode

Run JARVIS with additional debugging information:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Add this at the top of `jarvis.txt` to see detailed logs.

## Next Steps

Once you have JARVIS running successfully:

1. **Configure API keys**: See [Configuration Guide](configuration.md)
2. **Customize voice settings**: See [Configuration Guide](configuration.md)
3. **Add custom skills**: See [Skill Authoring Guide](skill-authoring.md)
4. **Learn the architecture**: See [Developer Guide](developer-guide.md)

---

**Need more help?** Check out the [Configuration Guide](configuration.md) or [Developer Guide](developer-guide.md).
