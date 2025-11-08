"""
Configuration loader and manager.
"""
import json
import os
from typing import Dict, Any


class ConfigLoader:
    """Load and manage configuration settings."""
    
    def __init__(self, config_path: str = None):
        """
        Args:
            config_path: Path to config JSON file. If None, uses default.
        """
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'config', 'default_config.json')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "simulation": {
                "autonomy_level": 0.75,
                "time_compression": 60,
                "interaction_density": "moderate",
                "narrative_coherence": "loose",
                "randomness": 0.25
            },
            "llm": {
                "enabled": False,
                "provider": "openai",
                "model": "gpt-4",
                "api_key_env_var": "OPENAI_API_KEY"
            },
            "output": {
                "save_directory": "./data/sessions"
            },
            "server": {
                "host": "127.0.0.1",
                "port": 5000,
                "debug": True
            }
        }
    
    def get(self, key_path: str, default=None):
        """
        Get a config value using dot notation.
        
        Example: config.get('simulation.autonomy_level')
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value):
        """
        Set a config value using dot notation.
        
        Example: config.set('simulation.autonomy_level', 0.8)
        """
        keys = key_path.split('.')
        target = self.config
        
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        target[keys[-1]] = value
    
    def save(self, path: str = None):
        """Save current configuration to file."""
        save_path = path or self.config_path
        
        with open(save_path, 'w') as f:
            json.dump(self.config, f, indent=2)


