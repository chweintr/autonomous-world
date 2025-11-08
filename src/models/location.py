"""
Location data models for the autonomous world system.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json


class TimeOfDay(Enum):
    """Time of day affecting location properties."""
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class Weather(Enum):
    """Weather conditions."""
    CLEAR = "clear"
    OVERCAST = "overcast"
    WINDY = "windy"
    DUSTY = "dusty"
    STORM_APPROACHING = "storm_approaching"
    RAIN = "rain"
    FOG = "fog"


@dataclass
class Location:
    """A distinct location in the world."""
    id: str
    name: str
    description: str  # general description of the space
    lighting_quality: str  # how light behaves here
    temperature_range: str  # hot, cool, varying, etc.
    acoustic_quality: str  # echoing, muffled, open, resonant
    objects_present: List[str]  # props and interactive objects
    architectural_features: List[str]  # walls, arches, patterns, etc.
    atmosphere: str  # overall mood of the space
    
    # Dynamic properties
    current_time: TimeOfDay = TimeOfDay.MIDDAY
    current_weather: Weather = Weather.CLEAR
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "lighting_quality": self.lighting_quality,
            "temperature_range": self.temperature_range,
            "acoustic_quality": self.acoustic_quality,
            "objects_present": self.objects_present,
            "architectural_features": self.architectural_features,
            "atmosphere": self.atmosphere,
            "current_time": self.current_time.value,
            "current_weather": self.current_weather.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Location':
        current_time = TimeOfDay(data.pop("current_time", "midday"))
        current_weather = Weather(data.pop("current_weather", "clear"))
        return cls(
            current_time=current_time,
            current_weather=current_weather,
            **data
        )
    
    def save_to_file(self, filepath: str):
        """Save location to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Location':
        """Load location from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def get_environmental_description(self) -> str:
        """Get a description of current environmental conditions."""
        time_descriptions = {
            TimeOfDay.DAWN: "first light breaking",
            TimeOfDay.MORNING: "morning light",
            TimeOfDay.MIDDAY: "harsh midday sun",
            TimeOfDay.AFTERNOON: "golden afternoon",
            TimeOfDay.DUSK: "fading light",
            TimeOfDay.NIGHT: "darkness",
            TimeOfDay.MIDNIGHT: "deep night"
        }
        
        weather_descriptions = {
            Weather.CLEAR: "clear sky",
            Weather.OVERCAST: "heavy clouds",
            Weather.WINDY: "strong wind",
            Weather.DUSTY: "dust in the air",
            Weather.STORM_APPROACHING: "storm gathering",
            Weather.RAIN: "rain falling",
            Weather.FOG: "thick fog"
        }
        
        return f"{time_descriptions[self.current_time]}, {weather_descriptions[self.current_weather]}"


