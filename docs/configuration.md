# Configuration Guide

Learn how to configure JARVIS for your specific needs, including API keys, voice settings, recognition parameters, and custom behaviors.

## Table of Contents

- [Configuration Methods](#configuration-methods)
- [API Configuration](#api-configuration)
- [Voice Settings](#voice-settings)
- [Recognition Settings](#recognition-settings)
- [Environment Variables](#environment-variables)
- [Advanced Configuration](#advanced-configuration)

## Configuration Methods

JARVIS supports multiple configuration approaches:

1. **Config File** (Recommended): `config.json` in project root
2. **Environment Variables**: For sensitive data like API keys
3. **Code Modification**: Direct editing of `jarvis.txt`

### Creating a Config File

Create `config.json` in your project root:

```json
{
  "voice": {
    "rate": 150,
    "volume": 0.9,
    "voice_index": 0
  },
  "recognition": {
    "pause_threshold": 1.0,
    "energy_threshold": 300,
    "language": "en-US"
  },
  "apis": {
    "openweathermap": {
      "api_key": "your_api_key_here",
      "city": "your_city",
      "units": "metric"
    },
    "wolframalpha": {
      "api_key": "your_api_key_here"
    }
  },
  "behavior": {
    "greeting_enabled": true,
    "verbose_logging": false
  }
}
```

> **⚠️ Security Note**: Add `config.json` to `.gitignore` to prevent committing API keys!

### Loading Configuration in Code

Add this to `jarvis.txt`:

```python
import json
import os

class Jarvis:
    def __init__(self, config_path='config.json'):
        # Load configuration
        self.config = self.load_config(config_path)
        
        # Initialize with config values
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        
        # Apply voice settings from config
        voice_config = self.config.get('voice', {})
        self.engine.setProperty('voice', self.voices[voice_config.get('voice_index', 0)].id)
        self.engine.setProperty('rate', voice_config.get('rate', 150))
        self.engine.setProperty('volume', voice_config.get('volume', 0.9))
        
        # Initialize recognizer with config
        self.recognizer = sr.Recognizer()
        rec_config = self.config.get('recognition', {})
        self.recognizer.pause_threshold = rec_config.get('pause_threshold', 1.0)
        self.recognizer.energy_threshold = rec_config.get('energy_threshold', 300)
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}  # Return empty dict if no config file
```

## API Configuration

### OpenWeatherMap API

Get weather data for your location.

#### Getting an API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key

#### Configuration

**Option 1: Config File**
```json
{
  "apis": {
    "openweathermap": {
      "api_key": "your_actual_api_key_here",
      "city": "London",
      "units": "metric"
    }
  }
}
```

**Option 2: Environment Variable**
```bash
# Windows
set OPENWEATHER_API_KEY=your_api_key_here

# macOS/Linux
export OPENWEATHER_API_KEY=your_api_key_here
```

**Option 3: Direct Code Edit**
```python
# In jarvis.txt, modify the weather command
api_key = os.environ.get('OPENWEATHER_API_KEY', 'your_fallback_key')
city = "London"  # Your city
```

#### Usage in Code

```python
def get_weather(self):
    """Get weather information"""
    api_key = self.config.get('apis', {}).get('openweathermap', {}).get('api_key')
    city = self.config.get('apis', {}).get('openweathermap', {}).get('city', 'London')
    units = self.config.get('apis', {}).get('openweathermap', {}).get('units', 'metric')
    
    if not api_key:
        self.speak("Weather API key not configured")
        return
    
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units={units}"
    
    try:
        response = requests.get(complete_url, timeout=5)
        data = response.json()
        
        if data.get("cod") != "404":
            main = data["main"]
            weather = data["weather"][0]
            
            temp = main["temp"]
            description = weather["description"]
            
            self.speak(f"The temperature in {city} is {temp} degrees")
            self.speak(f"Weather conditions are {description}")
        else:
            self.speak("City not found")
    except Exception as e:
        self.speak("Could not fetch weather data")
        print(f"Weather error: {e}")
```

### Wolfram Alpha API

For computational knowledge and calculations.

#### Getting an API Key

1. Visit [Wolfram Alpha Developer Portal](https://developer.wolframalpha.com/)
2. Sign up and create an application
3. Copy your App ID

#### Configuration

```json
{
  "apis": {
    "wolframalpha": {
      "api_key": "YOUR-APP-ID-HERE"
    }
  }
}
```

#### Usage Example

```python
import wolframalpha

def calculate_with_wolfram(self, query):
    """Use Wolfram Alpha for calculations"""
    api_key = self.config.get('apis', {}).get('wolframalpha', {}).get('api_key')
    
    if not api_key:
        self.speak("Wolfram Alpha API key not configured")
        return
    
    try:
        client = wolframalpha.Client(api_key)
        res = client.query(query)
        answer = next(res.results).text
        self.speak(answer)
        print(answer)
    except Exception as e:
        self.speak("Could not process the query")
        print(f"Wolfram error: {e}")
```

## Voice Settings

### Available Properties

| Property | Description | Default | Range |
|----------|-------------|---------|-------|
| `rate` | Speech speed (words per minute) | 200 | 50-400 |
| `volume` | Volume level | 1.0 | 0.0-1.0 |
| `voice` | Voice selection (male/female) | First available | Index |

### Listing Available Voices

```python
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for index, voice in enumerate(voices):
    print(f"{index}: {voice.name}")
    print(f"   ID: {voice.id}")
    print(f"   Languages: {voice.languages}")
    print(f"   Gender: {voice.gender}")
    print()
```

### Setting Voice Properties

```python
# In your Jarvis class __init__
self.engine = pyttsx3.init('sapi5')
self.voices = self.engine.getProperty('voices')

# Select voice (0 = male, 1 = female on most systems)
self.engine.setProperty('voice', self.voices[1].id)

# Set speech rate (slower = easier to understand)
self.engine.setProperty('rate', 150)  # 150 words per minute

# Set volume (0.0 to 1.0)
self.engine.setProperty('volume', 0.9)
```

### Voice Customization Examples

**Slow and Clear** (for accessibility)
```python
self.engine.setProperty('rate', 120)
self.engine.setProperty('volume', 1.0)
```

**Fast and Efficient**
```python
self.engine.setProperty('rate', 200)
self.engine.setProperty('volume', 0.8)
```

**Female Voice** (if available)
```python
# Try to set female voice
voices = self.engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        self.engine.setProperty('voice', voice.id)
        break
```

### Platform-Specific Voices

**Windows (SAPI5)**
- Built-in: David (male), Zira (female)
- Can add more via Windows Settings → Speech

**macOS**
- Many built-in voices
- System Preferences → Accessibility → Speech

**Linux (espeak)**
- Limited built-in voices
- Install more: `sudo apt-get install espeak-ng`

## Recognition Settings

### Key Parameters

```python
# Pause threshold: seconds of silence before phrase completes
self.recognizer.pause_threshold = 1.0  # Default: 0.8

# Energy threshold: minimum audio energy to consider for recording
self.recognizer.energy_threshold = 300  # Auto-adjusts if None

# Dynamic energy threshold: adjust to ambient noise
self.recognizer.dynamic_energy_threshold = True

# Phrase time limit: maximum seconds for a phrase
self.recognizer.phrase_time_limit = None  # No limit
```

### Environment-Specific Tuning

**Quiet Office**
```python
self.recognizer.energy_threshold = 300
self.recognizer.pause_threshold = 0.8
```

**Noisy Environment**
```python
self.recognizer.energy_threshold = 1000
self.recognizer.pause_threshold = 1.2
self.recognizer.dynamic_energy_threshold = True
```

**Low-Latency (Fast Response)**
```python
self.recognizer.pause_threshold = 0.5
self.recognizer.phrase_time_limit = 5  # 5 seconds max
```

### Ambient Noise Adjustment

```python
def take_command(self):
    """Listen for commands with ambient noise adjustment"""
    with sr.Microphone() as source:
        print("Calibrating for ambient noise... Please wait.")
        # Adjust for ambient noise for 2 seconds
        self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("Listening...")
        audio = self.recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = self.recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print("Could you please repeat that?")
        return "None"
```

### Language Configuration

Recognize different languages:

```python
# English (US)
query = self.recognizer.recognize_google(audio, language='en-US')

# English (UK)
query = self.recognizer.recognize_google(audio, language='en-GB')

# Spanish
query = self.recognizer.recognize_google(audio, language='es-ES')

# French
query = self.recognizer.recognize_google(audio, language='fr-FR')

# German
query = self.recognizer.recognize_google(audio, language='de-DE')
```

## Environment Variables

### Setting Environment Variables

**Windows (PowerShell)**
```powershell
# Set for current session
$env:OPENWEATHER_API_KEY="your_key"

# Set permanently
[System.Environment]::SetEnvironmentVariable('OPENWEATHER_API_KEY', 'your_key', 'User')
```

**Windows (CMD)**
```cmd
# Set for current session
set OPENWEATHER_API_KEY=your_key

# Set permanently
setx OPENWEATHER_API_KEY "your_key"
```

**macOS/Linux**
```bash
# Set for current session
export OPENWEATHER_API_KEY="your_key"

# Add to .bashrc or .zshrc for persistence
echo 'export OPENWEATHER_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

### Using Environment Variables in Code

```python
import os

# Get API key from environment variable with fallback
api_key = os.environ.get('OPENWEATHER_API_KEY', 'default_key')

# Get with error if not set
api_key = os.environ['OPENWEATHER_API_KEY']  # Raises KeyError if not set

# Get with config file fallback
api_key = os.environ.get(
    'OPENWEATHER_API_KEY',
    self.config.get('apis', {}).get('openweathermap', {}).get('api_key')
)
```

### Using .env Files

Create a `.env` file in project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_CITY=London
WOLFRAMALPHA_API_KEY=your_wolfram_key
```

Load with `python-dotenv`:

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now use them
api_key = os.environ.get('OPENWEATHER_API_KEY')
```

**Important**: Add `.env` to `.gitignore`!

## Advanced Configuration

### Custom Wake Word

Implement a custom wake word instead of always listening:

```python
def listen_for_wake_word(self):
    """Listen for 'Hey Jarvis' before processing commands"""
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = self.recognizer.listen(source)
        
    try:
        text = self.recognizer.recognize_google(audio).lower()
        if 'hey jarvis' in text or 'jarvis' in text:
            return True
    except:
        pass
    return False

def main():
    jarvis = Jarvis()
    jarvis.wish_me()
    
    while True:
        if jarvis.listen_for_wake_word():
            jarvis.speak("Yes?")
            query = jarvis.take_command()
            if query != 'None':
                jarvis.process_command(query)
```

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in your code
logger.info("JARVIS started")
logger.debug(f"Command received: {query}")
logger.error(f"Error processing command: {e}")
```

### Response Customization

```python
# Custom greeting messages
def wish_me(self):
    hour = datetime.datetime.now().hour
    
    greetings = {
        'morning': ["Good Morning!", "Rise and shine!", "Morning! Ready to be productive?"],
        'afternoon': ["Good Afternoon!", "Good day!", "Afternoon! How can I help?"],
        'evening': ["Good Evening!", "Evening!", "Good evening! What can I do for you?"]
    }
    
    import random
    
    if 0 <= hour < 12:
        greeting = random.choice(greetings['morning'])
    elif 12 <= hour < 18:
        greeting = random.choice(greetings['afternoon'])
    else:
        greeting = random.choice(greetings['evening'])
    
    self.speak(greeting)
    self.speak("I am Jarvis. How can I assist you today?")
```

### Timeout Configuration

```python
def take_command(self, timeout=5, phrase_time_limit=10):
    """Listen with configurable timeouts"""
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = self.recognizer.listen(
                source,
                timeout=timeout,  # Max time to wait for speech
                phrase_time_limit=phrase_time_limit  # Max phrase duration
            )
            
            query = self.recognizer.recognize_google(audio, language='en-US')
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return "None"
        except Exception as e:
            print(f"Error: {e}")
            return "None"
```

## Configuration Best Practices

### Security

1. **Never commit API keys to git**
   ```bash
   # Add to .gitignore
   config.json
   .env
   *.key
   ```

2. **Use environment variables for production**
3. **Rotate API keys regularly**
4. **Use read-only API keys when possible**

### Performance

1. **Cache API responses** when appropriate
2. **Set reasonable timeouts** to prevent hanging
3. **Adjust energy threshold** based on your environment
4. **Disable verbose logging** in production

### Maintainability

1. **Keep config separate from code**
2. **Document all configuration options**
3. **Provide sensible defaults**
4. **Validate configuration on startup**

### Example: Configuration Validation

```python
def validate_config(self):
    """Validate configuration on startup"""
    errors = []
    
    # Check API keys
    if not self.config.get('apis', {}).get('openweathermap', {}).get('api_key'):
        errors.append("OpenWeatherMap API key not configured")
    
    # Check voice settings
    voice_config = self.config.get('voice', {})
    rate = voice_config.get('rate', 150)
    if not 50 <= rate <= 400:
        errors.append(f"Invalid speech rate: {rate} (must be 50-400)")
    
    # Check recognition settings
    rec_config = self.config.get('recognition', {})
    threshold = rec_config.get('energy_threshold', 300)
    if threshold < 0:
        errors.append(f"Invalid energy threshold: {threshold}")
    
    if errors:
        print("Configuration warnings:")
        for error in errors:
            print(f"  - {error}")
    
    return len(errors) == 0
```

## Next Steps

- **Add custom skills**: See [Skill Authoring Guide](skill-authoring.md)
- **Understand the architecture**: See [Developer Guide](developer-guide.md)
- **Learn about memory**: See [Memory Internals](memory-internals.md)

---

**Questions?** Check the [Troubleshooting section](setup.md#troubleshooting) in the Setup Guide.
