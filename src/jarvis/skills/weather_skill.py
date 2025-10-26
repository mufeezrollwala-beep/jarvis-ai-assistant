from typing import Dict, Any
import requests
from .base_skill import BaseSkill, SkillResult


class WeatherSkill(BaseSkill):
    def __init__(self, api_key: str, default_city: str = "London"):
        self.api_key = api_key
        self.default_city = default_city
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_name(self) -> str:
        return "get_weather"
    
    def get_description(self) -> str:
        return "Get current weather information for a specified city"
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": f"The city name to get weather for (default: {self.default_city})",
                }
            },
            "required": [],
        }
    
    def execute(self, city: str = None, **kwargs) -> SkillResult:
        try:
            city = city or self.default_city
            
            if not self.api_key or self.api_key == "${OPENWEATHERMAP_API_KEY}":
                return SkillResult(
                    success=False,
                    result=None,
                    error="OpenWeatherMap API key not configured"
                )
            
            params = {
                "appid": self.api_key,
                "q": city,
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 404:
                return SkillResult(
                    success=False,
                    result=None,
                    error=f"City '{city}' not found"
                )
            
            response.raise_for_status()
            data = response.json()
            
            temp_kelvin = data["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            
            weather_info = {
                "city": city,
                "temperature_celsius": round(temp_celsius, 1),
                "temperature_fahrenheit": round(temp_fahrenheit, 1),
                "pressure": data["main"]["pressure"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
            }
            
            result_text = (
                f"Weather in {city}: {weather_info['description']}. "
                f"Temperature: {weather_info['temperature_celsius']}°C ({weather_info['temperature_fahrenheit']}°F). "
                f"Humidity: {weather_info['humidity']}%. "
                f"Pressure: {weather_info['pressure']} hPa."
            )
            
            return SkillResult(success=True, result=result_text)
        except requests.RequestException as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Error fetching weather data: {str(e)}"
            )
        except Exception as e:
            return SkillResult(
                success=False,
                result=None,
                error=f"Unexpected error: {str(e)}"
            )
