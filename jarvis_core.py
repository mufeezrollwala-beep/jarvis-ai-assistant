"""
Core command processing logic for Jarvis assistant
Shared by both voice and text interfaces
"""
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
from typing import Dict, Any


class JarvisCore:
    """Core logic for command processing shared by both voice and text interfaces"""
    
    def __init__(self):
        self.context = {}
        self.command_history = []
    
    def process_command(self, query: str) -> Dict[str, Any]:
        """
        Process user commands and return structured response
        
        Args:
            query: User command string
            
        Returns:
            Dictionary with response, status, and metadata
        """
        query = query.lower().strip()
        self.command_history.append({
            'query': query,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        response = {
            'success': True,
            'message': '',
            'data': None,
            'action': None
        }
        
        try:
            if 'wikipedia' in query:
                response['action'] = 'wikipedia_search'
                response['message'] = 'Searching Wikipedia...'
                search_query = query.replace("wikipedia", "").strip()
                results = wikipedia.summary(search_query, sentences=2)
                response['data'] = results
                response['message'] = f"According to Wikipedia: {results}"
                
            elif 'open youtube' in query:
                response['action'] = 'open_website'
                response['data'] = 'youtube.com'
                webbrowser.open("youtube.com")
                response['message'] = "Opening YouTube"
                
            elif 'open google' in query:
                response['action'] = 'open_website'
                response['data'] = 'google.com'
                webbrowser.open("google.com")
                response['message'] = "Opening Google"
                
            elif 'time' in query:
                response['action'] = 'get_time'
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                response['data'] = str_time
                response['message'] = f"The time is {str_time}"
                
            elif 'weather' in query:
                response['action'] = 'get_weather'
                api_key = os.environ.get('WEATHER_API_KEY', 'YOUR_WEATHER_API_KEY')
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                city = os.environ.get('WEATHER_CITY', 'London')
                complete_url = f"{base_url}appid={api_key}&q={city}"
                
                api_response = requests.get(complete_url)
                weather_data = api_response.json()
                
                if weather_data.get("cod") != "404":
                    main_data = weather_data.get("main", {})
                    temp_kelvin = main_data.get("temp", 0)
                    temp_celsius = temp_kelvin - 273.15
                    pressure = main_data.get("pressure", 0)
                    humidity = main_data.get("humidity", 0)
                    
                    response['data'] = {
                        'temperature_celsius': round(temp_celsius, 2),
                        'pressure': pressure,
                        'humidity': humidity,
                        'city': city
                    }
                    response['message'] = (
                        f"Weather in {city}: "
                        f"Temperature is {temp_celsius:.2f} degrees Celsius, "
                        f"Atmospheric pressure is {pressure} hPa, "
                        f"Humidity is {humidity} percent"
                    )
                else:
                    response['success'] = False
                    response['message'] = "City not found"
                    
            elif 'exit' in query or 'quit' in query or 'goodbye' in query:
                response['action'] = 'exit'
                response['message'] = "Goodbye!"
                
            else:
                response['action'] = 'unknown'
                response['message'] = "I'm not sure how to help with that. Try commands like 'time', 'wikipedia', 'open youtube', 'open google', or 'weather'."
                
        except Exception as e:
            response['success'] = False
            response['message'] = f"Error processing command: {str(e)}"
            response['data'] = {'error': str(e)}
            
        return response
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status and statistics"""
        return {
            'status': 'active',
            'uptime': time.time(),
            'commands_processed': len(self.command_history),
            'last_command': self.command_history[-1] if self.command_history else None
        }
    
    def get_greeting(self) -> str:
        """Get greeting based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        return f"{greeting} I am Jarvis. How can I help you?"
