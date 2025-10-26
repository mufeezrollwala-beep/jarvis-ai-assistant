# JARVIS Extension Examples

This directory contains example skills and extensions that demonstrate how to add new capabilities to JARVIS.

## Available Examples

### 1. Calculator Skill (`calculator_skill.py`)

A safe mathematical calculator that evaluates expressions without using `eval()`.

**Features:**
- Basic arithmetic (addition, subtraction, multiplication, division)
- Exponentiation and modulo operations
- Natural language input ("5 plus 3" or "5 + 3")
- Safe evaluation using AST (no code injection risks)

**Usage:**
```python
from examples.calculator_skill import CalculatorSkill

# In Jarvis.__init__()
self.calculator = CalculatorSkill(self)

# In process_command()
if self.calculator.can_handle(query):
    self.calculator.handle(query)
    return
```

**Voice Commands:**
- "Calculate 5 plus 3"
- "What is 10 divided by 2"
- "Calculate 2 to the power of 8"

---

### 2. News Headlines Skill (`news_skill.py`)

Fetch and read top news headlines from NewsAPI.

**Features:**
- Top headlines from various countries
- Category filtering (technology, business, sports, etc.)
- Configurable via config.json
- Source attribution

**Setup:**
1. Get free API key from [NewsAPI.org](https://newsapi.org/)
2. Add to `config.json`:
   ```json
   {
     "apis": {
       "news": {
         "api_key": "your_api_key_here",
         "country": "us",
         "category": "technology"
       }
     }
   }
   ```

**Voice Commands:**
- "Get news headlines"
- "Tell me technology news"
- "What's in the news?"

---

### 3. Reminder Skill (`reminder_skill.py`)

Set, view, and manage reminders with persistent storage.

**Features:**
- Time-based reminders
- Natural language time parsing ("at 3 PM", "tomorrow", "in 2 hours")
- Persistent JSON storage
- List and complete reminders
- Unique reminder IDs

**Usage:**
```python
from examples.reminder_skill import ReminderSkill

# In Jarvis.__init__()
self.reminder = ReminderSkill(self)

# In process_command()
if self.reminder.can_handle(query):
    self.reminder.handle(query)
    return
```

**Voice Commands:**
- "Remind me to call mom at 3 PM"
- "Set a reminder for tomorrow"
- "Show my reminders"
- "Complete reminder 1"

---

## Integration Guide

### Method 1: Direct Integration

Copy the skill into `jarvis.txt`:

```python
# At the top, add imports if needed
from datetime import datetime
import json

# In Jarvis class, add the skill methods
class Jarvis:
    def __init__(self):
        # ... existing initialization ...
        
        # Initialize your skill
        self.custom_skill_data = {}
    
    # Add skill methods here
    def my_custom_skill(self, query):
        # Skill implementation
        pass
    
    def process_command(self, query):
        """Process user commands"""
        
        # Add your skill trigger
        if 'my trigger' in query:
            self.my_custom_skill(query)
            return
        
        # ... existing commands ...
```

### Method 2: Import as Module

Create a modular structure:

```
jarvis-ai-assistant/
├── jarvis.txt (or jarvis.py)
├── skills/
│   ├── __init__.py
│   ├── calculator.py
│   ├── news.py
│   └── reminder.py
└── config.json
```

Then import in `jarvis.txt`:

```python
from skills.calculator import CalculatorSkill
from skills.news import NewsSkill
from skills.reminder import ReminderSkill

class Jarvis:
    def __init__(self):
        # ... existing initialization ...
        
        # Initialize skills
        self.skills = [
            CalculatorSkill(self),
            NewsSkill(self),
            ReminderSkill(self)
        ]
    
    def process_command(self, query):
        """Process commands using skills"""
        # Try each skill
        for skill in self.skills:
            if skill.can_handle(query):
                skill.handle(query)
                return
        
        # No skill matched
        self.speak("I'm not sure how to help with that")
```

### Method 3: Plugin System (Advanced)

Create a dynamic plugin loader:

```python
import os
import importlib

class SkillLoader:
    """Dynamically load skills from plugins directory"""
    
    def __init__(self, plugins_dir='plugins'):
        self.plugins_dir = plugins_dir
        self.skills = []
    
    def load_skills(self, jarvis_instance):
        """Load all skills from plugins directory"""
        if not os.path.exists(self.plugins_dir):
            return []
        
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('_skill.py'):
                module_name = filename[:-3]
                
                try:
                    # Import module
                    module = importlib.import_module(f'{self.plugins_dir}.{module_name}')
                    
                    # Find skill class
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            hasattr(attr, 'can_handle') and 
                            hasattr(attr, 'handle')):
                            # Instantiate skill
                            skill = attr(jarvis_instance)
                            self.skills.append(skill)
                            print(f"Loaded skill: {module_name}")
                
                except Exception as e:
                    print(f"Failed to load {module_name}: {e}")
        
        return self.skills
```

---

## Creating Your Own Skill

### Skill Template

```python
"""
Your Skill Name
================
Brief description of what your skill does.

Setup:
    Any setup instructions (API keys, dependencies, etc.)

Usage:
    - "Example command 1"
    - "Example command 2"
"""

class YourSkill:
    """Brief description"""
    
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        # Initialize any resources
    
    def can_handle(self, query):
        """
        Check if this skill can handle the query
        
        Args:
            query: User's voice command (lowercase)
        
        Returns:
            bool: True if skill can handle this query
        """
        triggers = ['trigger1', 'trigger2', 'trigger3']
        return any(trigger in query for trigger in triggers)
    
    def handle(self, query):
        """
        Execute the skill
        
        Args:
            query: User's voice command (lowercase)
        """
        try:
            # 1. Validate
            if not self._validate(query):
                self.jarvis.speak("Invalid input")
                return
            
            # 2. Process
            result = self._process(query)
            
            # 3. Respond
            if result:
                self.jarvis.speak(result)
            else:
                self.jarvis.speak("No result found")
        
        except Exception as e:
            self.jarvis.speak("Sorry, something went wrong")
            print(f"Error in {self.__class__.__name__}: {e}")
    
    def _validate(self, query):
        """Validate input"""
        # Your validation logic
        return True
    
    def _process(self, query):
        """Process the query"""
        # Your processing logic
        return "Result"
```

### Best Practices

1. **Error Handling**: Always wrap skill execution in try-except
2. **User Feedback**: Provide immediate feedback ("Working on that...")
3. **Configuration**: Use `self.jarvis.config` for settings
4. **Validation**: Validate all inputs before processing
5. **Documentation**: Include docstrings and usage examples
6. **Testing**: Test with various inputs and edge cases

### Testing Your Skill

```python
if __name__ == "__main__":
    # Mock Jarvis for testing
    class MockJarvis:
        def __init__(self):
            self.config = {}
        
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    # Test your skill
    jarvis = MockJarvis()
    skill = YourSkill(jarvis)
    
    test_queries = [
        "test command 1",
        "test command 2",
        "test edge case"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        if skill.can_handle(query):
            skill.handle(query)
        else:
            print("Skill cannot handle this query")
```

---

## Common Patterns

### Pattern 1: API Integration

```python
import requests

class APISkill:
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self.api_key = self._get_api_key()
        self.base_url = "https://api.example.com"
    
    def _get_api_key(self):
        return self.jarvis.config.get('apis', {}).get('service', {}).get('api_key')
    
    def _make_request(self, endpoint, params=None):
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
```

### Pattern 2: Persistent Storage

```python
import json
import os

class StorageSkill:
    def __init__(self, jarvis_instance, storage_file='data.json'):
        self.jarvis = jarvis_instance
        self.storage_file = storage_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_data()
        return self._default_data()
    
    def _save_data(self):
        """Save data to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Failed to save data: {e}")
    
    def _default_data(self):
        """Default data structure"""
        return {'items': []}
```

### Pattern 3: Natural Language Processing

```python
import re

class NLPSkill:
    def _extract_entities(self, query):
        """Extract named entities from query"""
        entities = {
            'numbers': self._extract_numbers(query),
            'dates': self._extract_dates(query),
            'locations': self._extract_locations(query)
        }
        return entities
    
    def _extract_numbers(self, text):
        """Extract numbers from text"""
        return [int(n) for n in re.findall(r'\d+', text)]
    
    def _extract_dates(self, text):
        """Extract date references"""
        date_words = ['today', 'tomorrow', 'yesterday', 'monday', 'tuesday']
        return [word for word in date_words if word in text.lower()]
    
    def _extract_locations(self, text):
        """Extract location names (simple)"""
        # In production, use spaCy or similar
        location_keywords = ['in', 'at', 'near']
        # Implementation here
        return []
```

---

## Resources

- **JARVIS Documentation**: See [docs/](../docs/) directory
- **Skill Authoring Guide**: [docs/skill-authoring.md](../docs/skill-authoring.md)
- **Developer Guide**: [docs/developer-guide.md](../docs/developer-guide.md)
- **API Documentation**: Check service provider docs
- **Python Libraries**: requests, json, datetime, re, ast

## Contributing

Have you created a useful skill? Share it with the community!

1. Test your skill thoroughly
2. Add documentation and examples
3. Create a pull request
4. Include usage examples and setup instructions

---

**Questions?** Open an issue or check the [Developer Guide](../docs/developer-guide.md).
