import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
import base64
import hashlib


class ConfigManager:
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or os.path.expanduser("~/.jarvis"))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.encrypted_file = self.config_dir / "credentials.enc"
        self.key_file = self.config_dir / ".key"
        self._config: Dict[str, Any] = {}
        self._credentials: Dict[str, Any] = {}
        self._cipher: Optional[Fernet] = None
        self._initialize_encryption()
        self.load_config()

    def _initialize_encryption(self):
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)
        self._cipher = Fernet(key)

    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self._config = json.load(f)

        if self.encrypted_file.exists():
            with open(self.encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self._cipher.decrypt(encrypted_data)
            self._credentials = json.loads(decrypted_data.decode('utf-8'))

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=2)
        os.chmod(self.config_file, 0o600)

        if self._credentials:
            encrypted_data = self._cipher.encrypt(
                json.dumps(self._credentials).encode('utf-8')
            )
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            os.chmod(self.encrypted_file, 0o600)

    def get_config(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set_config(self, key: str, value: Any):
        self._config[key] = value
        self.save_config()

    def get_credential(self, provider: str, key: str, default: Any = None) -> Any:
        return self._credentials.get(provider, {}).get(key, default)

    def set_credential(self, provider: str, key: str, value: Any):
        if provider not in self._credentials:
            self._credentials[provider] = {}
        self._credentials[provider][key] = value
        self.save_config()

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        return self._credentials.get(provider, {})

    def has_provider(self, provider: str) -> bool:
        return provider in self._credentials

    def remove_provider(self, provider: str):
        if provider in self._credentials:
            del self._credentials[provider]
            self.save_config()

    def list_providers(self) -> list:
        return list(self._credentials.keys())


class MockConfigManager(ConfigManager):
    def __init__(self):
        self.config_dir = Path("/tmp/.jarvis_mock")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.encrypted_file = self.config_dir / "credentials.enc"
        self.key_file = self.config_dir / ".key"
        self._config: Dict[str, Any] = {}
        self._credentials: Dict[str, Any] = self._get_mock_credentials()
        self._cipher: Optional[Fernet] = None
        self._initialize_encryption()

    def _get_mock_credentials(self) -> Dict[str, Any]:
        return {
            "home_assistant": {
                "url": "http://localhost:8123",
                "token": "mock_ha_token_12345",
                "websocket_url": "ws://localhost:8123/api/websocket"
            },
            "hue": {
                "bridge_ip": "192.168.1.100",
                "username": "mock_hue_username",
                "api_key": "mock_hue_api_key"
            },
            "tplink": {
                "username": "mock_tplink_user",
                "password": "mock_tplink_pass"
            }
        }
