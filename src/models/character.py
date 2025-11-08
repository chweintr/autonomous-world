"""
Character data models for the autonomous world system.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import json


class EmotionalState(Enum):
    """Possible emotional states for characters."""
    CALM = "calm"
    TENSE = "tense"
    EXUBERANT = "exuberant"
    MELANCHOLIC = "melancholic"
    CHARGED = "charged"
    UNCERTAIN = "uncertain"
    AGGRESSIVE = "aggressive"
    WITHDRAWN = "withdrawn"


@dataclass
class Memory:
    """A memory stored by a character."""
    timestamp: datetime
    memory_type: str  # "observation", "interaction", "dialogue", "event"
    content: str  # What happened/was said
    location: str  # Where it happened
    other_characters: List[str] = field(default_factory=list)  # Who was involved
    importance: float = 5.0  # 0-10, how significant
    emotional_impact: float = 0.0  # -1 to 1, emotional charge
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "memory_type": self.memory_type,
            "content": self.content,
            "location": self.location,
            "other_characters": self.other_characters,
            "importance": self.importance,
            "emotional_impact": self.emotional_impact
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def to_summary(self) -> str:
        """Short summary for context."""
        time_str = self.timestamp.strftime("%H:%M")
        others = ", ".join(self.other_characters) if self.other_characters else "alone"
        return f"[{time_str}] {self.content[:60]}... (with {others})"


@dataclass
class Animal:
    """Animal companion that externalizes suppressed impulses."""
    species: str  # horse, pig, bird, wolf, etc.
    name: str
    description: str  # physical appearance
    externalized_impulse: str  # what suppressed aspect of the character this represents
    temperament: str  # calm, skittish, aggressive, playful, etc.
    current_state: str = "neutral"  # current behavior state
    
    def to_dict(self) -> Dict:
        return {
            "species": self.species,
            "name": self.name,
            "description": self.description,
            "externalized_impulse": self.externalized_impulse,
            "temperament": self.temperament,
            "current_state": self.current_state
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Animal':
        return cls(**data)


@dataclass
class Character:
    """A persistent character in the world."""
    id: str
    name: str
    archetype: str  # biker, rider, handler, drifter, etc.
    physical_description: str  # clothing, posture, appearance
    backstory: str  # 200-300 words
    motivational_drivers: List[str]  # 3-5 core impulses
    relationships: Dict[str, str]  # character_id -> relationship description
    animal_companion: Animal
    
    # Dynamic state
    emotional_state: EmotionalState = EmotionalState.CALM
    current_location: Optional[str] = None
    emotional_intensity: float = 0.5  # 0.0 to 1.0
    
    # Memory system
    memory_stream: List[Memory] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "physical_description": self.physical_description,
            "backstory": self.backstory,
            "motivational_drivers": self.motivational_drivers,
            "relationships": self.relationships,
            "animal_companion": self.animal_companion.to_dict(),
            "emotional_state": self.emotional_state.value,
            "current_location": self.current_location,
            "emotional_intensity": self.emotional_intensity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        animal_data = data.pop("animal_companion")
        emotional_state = EmotionalState(data.pop("emotional_state", "calm"))
        return cls(
            animal_companion=Animal.from_dict(animal_data),
            emotional_state=emotional_state,
            **data
        )
    
    def save_to_file(self, filepath: str):
        """Save character to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Character':
        """Load character from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def shift_emotional_state(self, new_state: EmotionalState, intensity_delta: float = 0.0):
        """Shift character's emotional state."""
        self.emotional_state = new_state
        self.emotional_intensity = max(0.0, min(1.0, self.emotional_intensity + intensity_delta))
    
    def get_dominant_driver(self) -> str:
        """Get the currently most influential motivational driver."""
        # In future versions, this could be weighted by context
        import random
        return random.choice(self.motivational_drivers)
    
    # Memory methods
    def add_memory(self, memory: Memory):
        """Add a memory to the character's memory stream."""
        self.memory_stream.append(memory)
        
        # Prune old low-importance memories if too many
        if len(self.memory_stream) > 50:
            self._prune_memories()
    
    def _prune_memories(self):
        """Keep only recent or important memories."""
        # Keep last 20 memories regardless of importance
        recent = self.memory_stream[-20:]
        
        # Keep high-importance memories from before
        important = [m for m in self.memory_stream[:-20] if m.importance >= 7.0]
        
        # Combine
        self.memory_stream = important + recent
    
    def get_recent_memories(self, count: int = 5) -> List[Memory]:
        """Get most recent memories."""
        return self.memory_stream[-count:] if self.memory_stream else []
    
    def get_memories_about(self, character_id: str, limit: int = 3) -> List[Memory]:
        """Get memories involving another specific character."""
        relevant = [m for m in self.memory_stream 
                   if character_id in m.other_characters]
        return relevant[-limit:] if relevant else []
    
    def get_memories_at_location(self, location_id: str, limit: int = 3) -> List[Memory]:
        """Get memories from a specific location."""
        relevant = [m for m in self.memory_stream 
                   if m.location == location_id]
        return relevant[-limit:] if relevant else []
    
    def has_met_before(self, character_id: str) -> bool:
        """Check if this character has met another before."""
        return any(character_id in m.other_characters for m in self.memory_stream)


