import unittest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jarvis.config import load_config, Config


class TestConfig(unittest.TestCase):
    def test_config_get(self):
        config_dict = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "api_key": "test_key"
                }
            }
        }
        config = Config(config_dict)
        
        self.assertEqual(config.get("llm.provider"), "openai")
        self.assertEqual(config.get("llm.openai.api_key"), "test_key")
        self.assertIsNone(config.get("nonexistent"))
        self.assertEqual(config.get("nonexistent", "default"), "default")
    
    def test_env_var_expansion(self):
        os.environ["TEST_API_KEY"] = "my_secret_key"
        
        config_dict = {
            "api": {
                "key": "${TEST_API_KEY}"
            }
        }
        config = Config(config_dict)
        
        self.assertEqual(config.get("api.key"), "my_secret_key")
        
        del os.environ["TEST_API_KEY"]
    
    def test_load_config_from_file(self):
        config_content = """
llm:
  provider: openai
  openai:
    api_key: test_key
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            self.assertEqual(config.get("llm.provider"), "openai")
            self.assertEqual(config.get("llm.openai.api_key"), "test_key")
        finally:
            os.unlink(config_path)


if __name__ == "__main__":
    unittest.main()
