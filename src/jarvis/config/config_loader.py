import os
import yaml
from typing import Any, Dict
from pathlib import Path


class Config:
    def __init__(self, config_dict: Dict[str, Any]):
        self._config = config_dict
        self._expand_env_vars(self._config)
    
    def _expand_env_vars(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._expand_env_vars(value)
        elif isinstance(obj, list):
            return [self._expand_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            return os.path.expandvars(obj)
        return obj
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)


def load_config(config_path: str = None) -> Config:
    if config_path is None:
        config_path = os.path.join(os.getcwd(), "config.yaml")
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    return Config(config_dict)
