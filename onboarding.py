from typing import Dict, List, Optional
from memory_store import MemoryStore


class OnboardingManager:
    def __init__(self, memory_store: MemoryStore):
        self.memory = memory_store
    
    def run_onboarding(self, user_data: Optional[Dict] = None):
        print("\n=== Jarvis Onboarding ===")
        print("Let me learn about you to provide better assistance.\n")
        
        if user_data:
            self._load_user_data(user_data)
        else:
            self._interactive_onboarding()
        
        self._load_seed_knowledge()
        
        print("\n✓ Onboarding complete! I'm ready to assist you.\n")
    
    def _interactive_onboarding(self):
        print("Please provide some basic information (press Enter to skip):\n")
        
        name = input("Your name: ").strip()
        if name:
            self.memory.add_user_preference("user_name", name)
            print(f"Nice to meet you, {name}!")
        
        location = input("Your location/city: ").strip()
        if location:
            self.memory.add_user_preference("user_location", location)
        
        preferred_temperature = input("Preferred temperature unit (celsius/fahrenheit): ").strip().lower()
        if preferred_temperature in ['celsius', 'fahrenheit']:
            self.memory.add_user_preference("temperature_unit", preferred_temperature)
        
        time_format = input("Preferred time format (12/24): ").strip()
        if time_format in ['12', '24']:
            self.memory.add_user_preference("time_format", time_format)
        
        interests = input("Your interests (comma-separated): ").strip()
        if interests:
            self.memory.add_user_preference("user_interests", interests)
            for interest in interests.split(','):
                interest = interest.strip()
                if interest:
                    self.memory.long_term.add(
                        f"User is interested in {interest}",
                        {'category': 'interest', 'topic': interest}
                    )
    
    def _load_user_data(self, user_data: Dict):
        for key, value in user_data.items():
            self.memory.add_user_preference(key, str(value))
    
    def _load_seed_knowledge(self):
        seed_knowledge = [
            {
                'text': "I am Jarvis, an AI assistant designed to help with various tasks including web searches, information lookup, time queries, weather updates, and general conversation.",
                'metadata': {'category': 'system', 'type': 'identity'}
            },
            {
                'text': "I can search Wikipedia for information. Users can say 'Wikipedia' followed by their query.",
                'metadata': {'category': 'capability', 'command': 'wikipedia'}
            },
            {
                'text': "I can open YouTube and Google in the web browser upon request.",
                'metadata': {'category': 'capability', 'command': 'web'}
            },
            {
                'text': "I can tell the current time when asked.",
                'metadata': {'category': 'capability', 'command': 'time'}
            },
            {
                'text': "I can provide weather information if configured with an API key.",
                'metadata': {'category': 'capability', 'command': 'weather'}
            },
            {
                'text': "Users can exit the conversation by saying 'exit' or 'goodbye'.",
                'metadata': {'category': 'capability', 'command': 'exit'}
            },
        ]
        
        for knowledge in seed_knowledge:
            self.memory.long_term.add(knowledge['text'], knowledge['metadata'])
    
    def quick_setup(self, name: str, location: Optional[str] = None):
        self.memory.add_user_preference("user_name", name)
        
        if location:
            self.memory.add_user_preference("user_location", location)
        
        self._load_seed_knowledge()
        
        print(f"✓ Quick setup complete for {name}!")
    
    def check_onboarding_status(self) -> Dict[str, bool]:
        preferences = self.memory.get_all_preferences()
        
        status = {
            'has_user_name': 'user_name' in preferences,
            'has_location': 'user_location' in preferences,
            'has_seed_knowledge': len(self.memory.long_term.get_all()) > 0,
            'is_ready': 'user_name' in preferences or len(self.memory.long_term.get_all()) > 0
        }
        
        return status
    
    def add_device_knowledge(self, device_name: str, device_type: str, 
                           location: Optional[str] = None, capabilities: Optional[List[str]] = None):
        text = f"Home device: {device_name} ({device_type})"
        if location:
            text += f" located in {location}"
        
        metadata = {
            'category': 'device',
            'device_name': device_name,
            'device_type': device_type
        }
        
        if location:
            metadata['location'] = location
        
        self.memory.long_term.add(text, metadata)
        
        if capabilities:
            for capability in capabilities:
                cap_text = f"{device_name} can {capability}"
                cap_metadata = {
                    'category': 'device_capability',
                    'device_name': device_name,
                    'capability': capability
                }
                self.memory.long_term.add(cap_text, cap_metadata)
    
    def add_correction(self, original_query: str, correction: str):
        text = f"Correction learned: When user asks '{original_query}', they mean '{correction}'"
        metadata = {
            'category': 'correction',
            'original': original_query,
            'corrected': correction
        }
        self.memory.long_term.add(text, metadata)
