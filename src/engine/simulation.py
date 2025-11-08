"""
Main simulation engine that orchestrates the autonomous world.
"""
import random
from typing import Dict, List, Optional
from datetime import datetime

from src.models.character import Character, EmotionalState, Memory
from src.models.location import Location
from src.models.interaction import Interaction, InteractionType, EmotionalTemperature
from src.engine.world_state import WorldState
from src.engine.decision_engine import DecisionEngine, ActionType, Decision
from src.generators.description_generator import DescriptionGenerator


class SimulationConfig:
    """Configuration for simulation parameters."""
    
    def __init__(
        self,
        autonomy_level: float = 0.75,
        time_compression: int = 60,
        interaction_density: str = "moderate",
        narrative_coherence: str = "loose",
        randomness: float = 0.25
    ):
        self.autonomy_level = autonomy_level  # 0.0-1.0
        self.time_compression = time_compression  # real minutes to sim minutes
        self.interaction_density = interaction_density  # sparse, moderate, dense
        self.narrative_coherence = narrative_coherence  # loose, tight
        self.randomness = randomness  # 0.0-1.0
        
        # Convert density to time between actions
        density_map = {
            "sparse": 10,  # action every 10 sim minutes
            "moderate": 5,
            "dense": 2
        }
        self.minutes_per_action = density_map.get(interaction_density, 5)


class Simulation:
    """Main simulation orchestrator."""
    
    def __init__(
        self,
        world_state: WorldState,
        config: SimulationConfig,
        use_llm: bool = False,
        llm_api_key: Optional[str] = None
    ):
        self.world = world_state
        self.config = config
        self.decision_engine = DecisionEngine(
            autonomy_level=config.autonomy_level,
            randomness=config.randomness
        )
        self.description_generator = DescriptionGenerator(
            use_llm=use_llm,
            api_key=llm_api_key
        )
        self.is_running = False
        self.emergence_tracker = EmergenceTracker()
    
    def seed_scenario(self, character_placements: Dict[str, str]):
        """
        Place characters in locations to start a scenario.
        
        Args:
            character_placements: {character_id: location_id}
        """
        for char_id, loc_id in character_placements.items():
            if char_id in self.world.characters and loc_id in self.world.locations:
                self.world.characters[char_id].current_location = loc_id
    
    def run_simulation(self, duration_minutes: float, callback=None):
        """
        Run simulation for specified duration.
        
        Args:
            duration_minutes: How long to run (in simulated time)
            callback: Optional callback function called after each interaction
        """
        self.is_running = True
        elapsed = 0
        
        while elapsed < duration_minutes and self.is_running:
            # Each cycle represents a time step
            time_step = self.config.minutes_per_action
            
            # Select active characters (those currently at locations)
            active_characters = [c for c in self.world.characters.values() 
                               if c.current_location is not None]
            
            if not active_characters:
                break
            
            # Pick a character to act this cycle
            acting_character = random.choice(active_characters)
            
            # Get context
            current_location = self.world.locations[acting_character.current_location]
            other_chars = [c for c in self.world.get_characters_at_location(
                acting_character.current_location) if c.id != acting_character.id]
            
            # Decide action
            decision = self.decision_engine.decide_action(
                acting_character,
                current_location,
                self.world.locations,
                other_chars
            )
            
            # Execute action and generate interaction
            interaction = self._execute_decision(
                acting_character,
                decision,
                current_location,
                other_chars
            )
            
            if interaction:
                self.world.add_interaction(interaction)
                self.emergence_tracker.track(interaction, acting_character)
                
                if callback:
                    callback(interaction)
            
            # Advance time
            self.world.advance_time(time_step)
            elapsed += time_step
        
        self.is_running = False
    
    def _execute_decision(
        self,
        character: Character,
        decision: Decision,
        location: Location,
        other_characters: List[Character]
    ) -> Optional[Interaction]:
        """Execute a character's decision and create an interaction."""
        
        # Determine interaction type
        if decision.action_type == ActionType.MOVE_TO_LOCATION:
            # Move character
            if decision.target in self.world.locations:
                character.current_location = decision.target
                location = self.world.locations[decision.target]
                interaction_type = InteractionType.OBSERVATION
            else:
                return None
        
        elif decision.action_type == ActionType.INTERACT_WITH_CHARACTER:
            interaction_type = InteractionType.CHARACTER_TO_CHARACTER
        
        elif decision.action_type == ActionType.INTERACT_WITH_ANIMAL:
            interaction_type = InteractionType.CHARACTER_TO_ANIMAL
        
        elif decision.action_type == ActionType.INTERACT_WITH_ENVIRONMENT:
            interaction_type = InteractionType.CHARACTER_TO_ENVIRONMENT
        
        else:  # OBSERVE
            interaction_type = InteractionType.OBSERVATION
        
        # Get all characters and animals at this location
        chars_present = self.world.get_characters_at_location(character.current_location)
        animals_present = self.world.get_animals_at_location(character.current_location)
        
        # Generate description
        action_desc, material_details, emotional_temp = self.description_generator.generate_interaction_description(
            interaction_type,
            location,
            chars_present,
            decision.reasoning,
            location.current_time.value,
            location.current_weather.value
        )
        
        # Create interaction
        interaction = Interaction(
            timestamp=self.world.current_time,
            location_id=location.id,
            location_name=location.name,
            interaction_type=interaction_type,
            characters_present=[c.id for c in chars_present],
            animals_present=animals_present,
            action_description=action_desc,
            material_details=material_details,
            emotional_temperature=emotional_temp,
            time_of_day=location.current_time.value,
            weather=location.current_weather.value,
            environmental_context=location.get_environmental_description(),
            is_unexpected=decision.is_random
        )
        
        # Update character emotional state based on interaction
        self._update_character_state(character, interaction, decision)
        
        # Store memories for all characters present
        self._store_memories(interaction, chars_present)
        
        return interaction
    
    def _update_character_state(self, character: Character, 
                               interaction: Interaction,
                               decision: Decision):
        """Update character's emotional state based on interaction."""
        
        # Map emotional temperature to character state
        temp_to_state = {
            EmotionalTemperature.TENSE: EmotionalState.TENSE,
            EmotionalTemperature.EXUBERANT: EmotionalState.EXUBERANT,
            EmotionalTemperature.UNCERTAIN: EmotionalState.UNCERTAIN,
            EmotionalTemperature.CHARGED: EmotionalState.CHARGED,
            EmotionalTemperature.MELANCHOLIC: EmotionalState.MELANCHOLIC,
            EmotionalTemperature.AGGRESSIVE: EmotionalState.AGGRESSIVE,
            EmotionalTemperature.TENDER: EmotionalState.CALM,
            EmotionalTemperature.PLAYFUL: EmotionalState.EXUBERANT,
            EmotionalTemperature.RITUAL: EmotionalState.CALM,
            EmotionalTemperature.RUPTURED: EmotionalState.AGGRESSIVE
        }
        
        new_state = temp_to_state.get(interaction.emotional_temperature, character.emotional_state)
        
        # Shift intensity slightly
        intensity_delta = 0.1 if decision.is_random else 0.05
        if interaction.emotional_temperature in [EmotionalTemperature.TENSE, 
                                                 EmotionalTemperature.CHARGED,
                                                 EmotionalTemperature.AGGRESSIVE]:
            intensity_delta = 0.15
        
        character.shift_emotional_state(new_state, intensity_delta)
    
    def _store_memories(self, interaction: Interaction, characters_present: List[Character]):
        """Store memories of this interaction for all characters present."""
        
        # Calculate importance (based on emotional charge, unexpectedness, etc.)
        importance = 5.0  # Base importance
        
        if interaction.is_unexpected:
            importance += 2.0
        
        if interaction.emotional_temperature in [EmotionalTemperature.CHARGED, 
                                                 EmotionalTemperature.TENSE,
                                                 EmotionalTemperature.RUPTURED]:
            importance += 1.5
        
        if len(characters_present) > 2:
            importance += 1.0
        
        importance = min(10.0, importance)
        
        # Calculate emotional impact
        emotional_impact_map = {
            EmotionalTemperature.TENDER: 0.5,
            EmotionalTemperature.PLAYFUL: 0.3,
            EmotionalTemperature.CHARGED: 0.8,
            EmotionalTemperature.TENSE: -0.3,
            EmotionalTemperature.AGGRESSIVE: -0.7,
            EmotionalTemperature.MELANCHOLIC: -0.5,
            EmotionalTemperature.UNCERTAIN: 0.0,
            EmotionalTemperature.EXUBERANT: 0.6,
            EmotionalTemperature.RITUAL: 0.2,
            EmotionalTemperature.RUPTURED: -0.9
        }
        
        emotional_impact = emotional_impact_map.get(interaction.emotional_temperature, 0.0)
        
        # Store memory for each character
        for char in characters_present:
            other_chars = [c.id for c in characters_present if c.id != char.id]
            
            memory = Memory(
                timestamp=interaction.timestamp,
                memory_type="interaction" if other_chars else "observation",
                content=interaction.action_description,
                location=interaction.location_id,
                other_characters=other_chars,
                importance=importance,
                emotional_impact=emotional_impact
            )
            
            char.add_memory(memory)
    
    def stop(self):
        """Stop the simulation."""
        self.is_running = False
    
    def get_emergence_report(self) -> str:
        """Get report on emergent patterns."""
        return self.emergence_tracker.generate_report()


class EmergenceTracker:
    """Tracks and identifies emergent patterns in the simulation."""
    
    def __init__(self):
        self.character_location_counts: Dict[str, Dict[str, int]] = {}
        self.character_pair_counts: Dict[tuple, int] = {}
        self.animal_behavior_counts: Dict[str, int] = {}
        self.location_emotional_temps: Dict[str, List[EmotionalTemperature]] = {}
        self.unexpected_events: List[Interaction] = []
    
    def track(self, interaction: Interaction, primary_character: Character):
        """Track an interaction for pattern detection."""
        
        # Track character location preferences
        if primary_character.id not in self.character_location_counts:
            self.character_location_counts[primary_character.id] = {}
        
        loc_id = interaction.location_id
        self.character_location_counts[primary_character.id][loc_id] = \
            self.character_location_counts[primary_character.id].get(loc_id, 0) + 1
        
        # Track character pairings
        if len(interaction.characters_present) > 1:
            pair = tuple(sorted(interaction.characters_present[:2]))
            self.character_pair_counts[pair] = self.character_pair_counts.get(pair, 0) + 1
        
        # Track location emotional temperatures
        if loc_id not in self.location_emotional_temps:
            self.location_emotional_temps[loc_id] = []
        self.location_emotional_temps[loc_id].append(interaction.emotional_temperature)
        
        # Track unexpected events
        if interaction.is_unexpected:
            self.unexpected_events.append(interaction)
    
    def generate_report(self) -> str:
        """Generate a report on emergent patterns."""
        report = "# EMERGENCE PATTERNS\n\n"
        
        # Character location tendencies
        report += "## Location Tendencies\n"
        for char_id, locations in self.character_location_counts.items():
            if locations:
                favorite = max(locations.items(), key=lambda x: x[1])
                report += f"- {char_id}: Gravitates toward {favorite[0]} ({favorite[1]} visits)\n"
        
        # Character pairings
        report += "\n## Recurring Pairings\n"
        significant_pairs = [(pair, count) for pair, count in self.character_pair_counts.items() 
                           if count >= 3]
        if significant_pairs:
            for pair, count in sorted(significant_pairs, key=lambda x: x[1], reverse=True):
                report += f"- {pair[0]} + {pair[1]}: {count} interactions\n"
        else:
            report += "No significant recurring pairings yet.\n"
        
        # Location atmospheres
        report += "\n## Location Atmospheres\n"
        for loc_id, temps in self.location_emotional_temps.items():
            if temps:
                most_common = max(set(temps), key=temps.count)
                report += f"- {loc_id}: Tends toward {most_common.value} ({temps.count(most_common)}/{len(temps)})\n"
        
        # Unexpected moments
        report += f"\n## Emergent/Unexpected Events: {len(self.unexpected_events)}\n"
        if self.unexpected_events:
            report += "Recent unexpected moments:\n"
            for event in self.unexpected_events[-5:]:
                report += f"- [{event.timestamp.strftime('%H:%M')}] {event.location_name}: {event.action_description[:80]}...\n"
        
        return report


