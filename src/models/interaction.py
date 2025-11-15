"""
Interaction data models for the autonomous world system.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class InteractionType(Enum):
    """Types of interactions possible in the world."""
    CHARACTER_TO_CHARACTER = "character_to_character"
    CHARACTER_TO_ANIMAL = "character_to_animal"
    CHARACTER_TO_ENVIRONMENT = "character_to_environment"
    ANIMAL_TO_ANIMAL = "animal_to_animal"
    ANIMAL_TO_ENVIRONMENT = "animal_to_environment"
    OBSERVATION = "observation"  # No interaction, just presence


class EmotionalTemperature(Enum):
    """Overall emotional quality of a moment."""
    TENSE = "tense"
    EXUBERANT = "exuberant"
    UNCERTAIN = "uncertain"
    CHARGED = "charged"
    MELANCHOLIC = "melancholic"
    PLAYFUL = "playful"
    AGGRESSIVE = "aggressive"
    TENDER = "tender"
    RITUAL = "ritual"
    RUPTURED = "ruptured"


@dataclass
class Interaction:
    """A single interaction event in the simulation."""
    timestamp: datetime
    location_id: str
    location_name: str
    interaction_type: InteractionType
    characters_present: List[str]  # character IDs
    animals_present: List[str]  # animal names
    
    # The core content
    action_description: str  # 2-3 sentences, vivid and specific
    material_details: str  # what would be visible
    emotional_temperature: EmotionalTemperature

    # Metadata
    time_of_day: str
    weather: str
    environmental_context: str

    # Optional fields (must come after required fields)
    cinematic_report: str = ""  # Camera movement, framing, scene composition

    # Flags for emergence tracking
    is_unexpected: bool = False
    pattern_tags: List[str] = field(default_factory=list)
    
    def to_field_note(self) -> str:
        """Format interaction as a field note."""
        time_str = self.timestamp.strftime("%H:%M")

        note = f"[{time_str} - {self.location_name} - {self.time_of_day.title()}]\n"
        note += f"{self.action_description}\n\n"
        note += f"Material details: {self.material_details}\n"

        if self.cinematic_report:
            note += f"\nCinematic framing: {self.cinematic_report}\n"

        note += f"Emotional temperature: {self.emotional_temperature.value.title()}"

        if self.is_unexpected:
            note += " [EMERGENT BEHAVIOR]"

        if self.pattern_tags:
            note += f"\nPatterns: {', '.join(self.pattern_tags)}"

        return note
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "location_id": self.location_id,
            "location_name": self.location_name,
            "interaction_type": self.interaction_type.value,
            "characters_present": self.characters_present,
            "animals_present": self.animals_present,
            "action_description": self.action_description,
            "material_details": self.material_details,
            "cinematic_report": self.cinematic_report,
            "emotional_temperature": self.emotional_temperature.value,
            "time_of_day": self.time_of_day,
            "weather": self.weather,
            "environmental_context": self.environmental_context,
            "is_unexpected": self.is_unexpected,
            "pattern_tags": self.pattern_tags
        }


