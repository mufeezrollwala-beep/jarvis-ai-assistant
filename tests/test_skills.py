import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jarvis.skills import (
    WikipediaSkill,
    WebBrowserSkill,
    TimeSkill,
    WeatherSkill,
)


class TestWikipediaSkill(unittest.TestCase):
    def setUp(self):
        self.skill = WikipediaSkill()
    
    def test_get_name(self):
        self.assertEqual(self.skill.get_name(), "search_wikipedia")
    
    def test_get_description(self):
        description = self.skill.get_description()
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
    
    def test_get_parameters(self):
        params = self.skill.get_parameters()
        self.assertIn("properties", params)
        self.assertIn("query", params["properties"])
    
    def test_to_tool_definition(self):
        tool_def = self.skill.to_tool_definition()
        self.assertEqual(tool_def["type"], "function")
        self.assertEqual(tool_def["function"]["name"], "search_wikipedia")


class TestWebBrowserSkill(unittest.TestCase):
    def setUp(self):
        self.skill = WebBrowserSkill()
    
    def test_get_name(self):
        self.assertEqual(self.skill.get_name(), "open_website")
    
    def test_get_description(self):
        description = self.skill.get_description()
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
    
    def test_get_parameters(self):
        params = self.skill.get_parameters()
        self.assertIn("properties", params)
        self.assertIn("site", params["properties"])


class TestTimeSkill(unittest.TestCase):
    def setUp(self):
        self.skill = TimeSkill()
    
    def test_get_name(self):
        self.assertEqual(self.skill.get_name(), "get_current_time")
    
    def test_execute(self):
        result = self.skill.execute()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.result)
        self.assertRegex(result.result, r'\d{2}:\d{2}:\d{2}')


class TestWeatherSkill(unittest.TestCase):
    def setUp(self):
        self.skill = WeatherSkill(api_key="test_key", default_city="London")
    
    def test_get_name(self):
        self.assertEqual(self.skill.get_name(), "get_weather")
    
    def test_get_description(self):
        description = self.skill.get_description()
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
    
    def test_missing_api_key(self):
        skill = WeatherSkill(api_key="${OPENWEATHERMAP_API_KEY}")
        result = skill.execute(city="London")
        self.assertFalse(result.success)
        self.assertIn("not configured", result.error)


if __name__ == "__main__":
    unittest.main()
