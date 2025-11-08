"""
World state management for the autonomous world simulation.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os

from src.models.character import Character
from src.models.location import Location, TimeOfDay, Weather
from src.models.interaction import Interaction


class WorldState:
    """Manages the current state of the simulation world."""
    
    def __init__(self, characters: Dict[str, Character], locations: Dict[str, Location]):
        self.characters = characters
        self.locations = locations
        self.current_time = datetime.now()
        self.simulation_start_time = datetime.now()
        self.time_compression = 60  # 1 real minute = 60 simulated minutes
        self.interactions_log: List[Interaction] = []
        
    def advance_time(self, minutes: float):
        """Advance simulation time."""
        self.current_time += timedelta(minutes=minutes)
        self._update_environmental_conditions()
    
    def _update_environmental_conditions(self):
        """Update time of day and weather based on current time."""
        hour = self.current_time.hour
        
        # Update time of day for all locations
        if 5 <= hour < 7:
            time_of_day = TimeOfDay.DAWN
        elif 7 <= hour < 11:
            time_of_day = TimeOfDay.MORNING
        elif 11 <= hour < 14:
            time_of_day = TimeOfDay.MIDDAY
        elif 14 <= hour < 18:
            time_of_day = TimeOfDay.AFTERNOON
        elif 18 <= hour < 20:
            time_of_day = TimeOfDay.DUSK
        elif 20 <= hour < 24:
            time_of_day = TimeOfDay.NIGHT
        else:
            time_of_day = TimeOfDay.MIDNIGHT
        
        for location in self.locations.values():
            location.current_time = time_of_day
            # Weather changes could be more sophisticated
            # For now, keep it stable unless we implement weather events
    
    def get_characters_at_location(self, location_id: str) -> List[Character]:
        """Get all characters currently at a location."""
        return [char for char in self.characters.values() 
                if char.current_location == location_id]
    
    def get_animals_at_location(self, location_id: str) -> List[str]:
        """Get names of all animals at a location."""
        characters = self.get_characters_at_location(location_id)
        return [char.animal_companion.name for char in characters]
    
    def add_interaction(self, interaction: Interaction):
        """Log an interaction."""
        self.interactions_log.append(interaction)
    
    def get_recent_interactions(self, count: int = 10) -> List[Interaction]:
        """Get the most recent interactions."""
        return self.interactions_log[-count:]
    
    def save_session(self, session_name: str, output_dir: str):
        """Save the current session as a markdown field note."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{session_name}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"# Session: {session_name}\n")
            f.write(f"Started: {self.simulation_start_time.strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Duration: {(self.current_time - self.simulation_start_time).total_seconds() / 60:.1f} simulated minutes\n")
            f.write(f"Interactions logged: {len(self.interactions_log)}\n\n")
            f.write("---\n\n")
            
            for interaction in self.interactions_log:
                f.write(interaction.to_field_note())
                f.write("\n\n---\n\n")
        
        return filepath
    
    @classmethod
    def load_characters_from_directory(cls, directory: str) -> Dict[str, Character]:
        """Load all character files from a directory."""
        characters = {}
        for filename in os.listdir(directory):
            # Skip hidden files and macOS metadata files
            if filename.startswith('.') or filename.startswith('._'):
                continue
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                char = Character.load_from_file(filepath)
                characters[char.id] = char
        return characters
    
    @classmethod
    def load_locations_from_directory(cls, directory: str) -> Dict[str, Location]:
        """Load all location files from a directory."""
        locations = {}
        for filename in os.listdir(directory):
            # Skip hidden files and macOS metadata files
            if filename.startswith('.') or filename.startswith('._'):
                continue
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                loc = Location.load_from_file(filepath)
                locations[loc.id] = loc
        return locations

