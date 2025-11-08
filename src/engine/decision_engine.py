"""
Character decision-making engine with autonomous behavior.
"""
import random
from typing import List, Dict, Optional, Tuple
from enum import Enum

from src.models.character import Character, EmotionalState
from src.models.location import Location


class ActionType(Enum):
    """Possible action types characters can take."""
    MOVE_TO_LOCATION = "move_to_location"
    INTERACT_WITH_CHARACTER = "interact_with_character"
    INTERACT_WITH_ANIMAL = "interact_with_animal"
    INTERACT_WITH_ENVIRONMENT = "interact_with_environment"
    OBSERVE = "observe"
    LEAVE = "leave"


class Decision:
    """A character's decision about what to do next."""
    
    def __init__(self, action_type: ActionType, target: Optional[str] = None, 
                 reasoning: str = "", is_random: bool = False):
        self.action_type = action_type
        self.target = target  # location_id, character_id, object name, etc.
        self.reasoning = reasoning
        self.is_random = is_random


class DecisionEngine:
    """Makes autonomous decisions for characters based on their drivers and context."""
    
    def __init__(self, autonomy_level: float = 0.75, randomness: float = 0.25):
        """
        Args:
            autonomy_level: 0.0-1.0, how much characters follow their drivers
            randomness: 0.0-1.0, how much unpredictability in decisions
        """
        self.autonomy_level = autonomy_level
        self.randomness = randomness
    
    def decide_action(self, character: Character, current_location: Location,
                     available_locations: Dict[str, Location],
                     other_characters_present: List[Character]) -> Decision:
        """
        Decide what action a character should take.
        
        This combines:
        - Character's motivational drivers
        - Current emotional state
        - Environmental context
        - Presence of other characters
        - Randomness
        """
        # If other characters present, strongly prefer interaction (70% of time)
        if other_characters_present and random.random() < 0.7:
            target = random.choice(other_characters_present)
            
            # Check if they've met before - informs interaction
            has_history = character.has_met_before(target.id)
            past_meetings = character.get_memories_about(target.id, limit=2)
            
            # Build specific interaction context based on character + history
            context = self._build_interaction_context(
                character, target, has_history, past_meetings
            )
            
            return Decision(
                ActionType.INTERACT_WITH_CHARACTER, 
                target.id,
                context,
                is_random=False
            )
        
        # Randomness check - sometimes do something unexpected
        if random.random() < self.randomness:
            return self._make_random_decision(character, available_locations, 
                                             other_characters_present, current_location)
        
        # Get dominant driver
        driver = character.get_dominant_driver()
        
        # Decision based on archetype and driver
        decision = self._decide_based_on_driver(character, driver, current_location,
                                                available_locations, other_characters_present)
        
        return decision
    
    def _build_interaction_context(self, character: Character, target: Character,
                                   has_history: bool, past_meetings: List) -> str:
        """Build specific context for character interaction based on their nature and history."""
        
        # Character-specific interaction tendencies
        interaction_templates = {
            "measurer": [
                f"Measurer wants to measure something about {target.name}",
                f"Measurer notices {target.name} and wants to quantify their presence",
                f"Measurer stops to measure the distance to {target.name}"
            ],
            "collector": [
                f"Collector asks {target.name} if they've lost anything",
                f"Collector wants to return something dropped to {target.name}",
                f"Collector picks up a word {target.name} dropped"
            ],
            "knows_too_much": [
                f"The One Who Knows comments on simulation parameters to {target.name}",
                f"The One Who Knows asks {target.name} if they feel scripted",
                f"The One Who Knows references meta-reality to {target.name}"
            ],
            "backward": [
                f"Backward speaks to {target.name} about the past as if it's ahead",
                f"Backward backs away while talking to {target.name}",
                f"Backward gives {target.name} backward directions"
            ],
            "listener": [
                f"The Listener responds to something {target.name} didn't say",
                f"The Listener mishears {target.name}'s words",
                f"The Listener answers a question {target.name} didn't ask"
            ],
            "forget_nothing": [
                f"Forget-Nothing corrects {target.name} about a detail from the past",
                f"Forget-Nothing reminds {target.name} of something they said years ago",
                f"Forget-Nothing is working while {target.name} approaches"
            ],
            "parade": [
                f"Parade invites {target.name} to a ceremony that doesn't exist yet",
                f"Parade assigns {target.name} a role in an imaginary parade",
                f"Parade decorates the space around {target.name}"
            ],
            "tuesday": [
                f"Tuesday is asked about the suitcase by {target.name}",
                f"Tuesday smiles at {target.name} without explaining",
                f"{target.name} asks Tuesday about the suitcase"
            ],
            "bird_gatherer": [
                f"Bird Gatherer is asked by {target.name} why birds come",
                f"Bird Gatherer offers to repair something for {target.name}",
                f"Bird Gatherer and {target.name} work on something in silence"
            ],
            "witness": [
                f"Witness observes {target.name} and documents silently",
                f"{target.name} notices Witness watching",
                f"Witness and {target.name} share silent proximity"
            ],
            "sleeper": [
                f"Sleeper responds to {target.name} after a 3-second delay",
                f"{target.name} speaks to Sleeper who may be asleep",
                f"Sleeper says something dream-like to {target.name}"
            ]
        }
        
        # Get character-specific templates
        templates = interaction_templates.get(character.id, [
            f"{character.name} approaches {target.name}",
            f"{character.name} engages with {target.name}"
        ])
        
        base_context = random.choice(templates)
        
        # Add history context if they've met before
        if has_history and past_meetings:
            last_meeting = past_meetings[-1]
            time_ago = "recently" if len(character.memory_stream) < 10 else "earlier"
            base_context += f". They met {time_ago}: {last_meeting.content[:40]}..."
        
        return base_context
    
    def _make_random_decision(self, character: Character, available_locations: Dict[str, Location],
                             other_characters_present: List[Character],
                             current_location: Location) -> Decision:
        """Make a random, potentially unexpected decision."""
        action_types = list(ActionType)
        action = random.choice(action_types)
        
        if action == ActionType.MOVE_TO_LOCATION:
            target = random.choice(list(available_locations.keys()))
            return Decision(action, target, "Spontaneous movement", is_random=True)
        
        elif action == ActionType.INTERACT_WITH_CHARACTER:
            if other_characters_present:
                target = random.choice(other_characters_present).id
                return Decision(action, target, "Unexpected interaction", is_random=True)
        
        elif action == ActionType.INTERACT_WITH_ENVIRONMENT:
            if current_location.objects_present:
                target = random.choice(current_location.objects_present)
                return Decision(action, target, "Spontaneous object interaction", is_random=True)
        
        # Default to observation
        return Decision(ActionType.OBSERVE, None, "Random pause", is_random=True)
    
    def _decide_based_on_driver(self, character: Character, driver: str,
                                current_location: Location,
                                available_locations: Dict[str, Location],
                                other_characters_present: List[Character]) -> Decision:
        """Make decision based on character's motivational driver."""
        
        # Witness
        if character.id == "witness":
            if other_characters_present:
                return Decision(ActionType.OBSERVE, None, "Documenting interaction")
            else:
                return Decision(ActionType.OBSERVE, None, "Waiting for something to document")
        
        # Bird Gatherer
        elif character.id == "bird_gatherer":
            if "repair" in driver.lower():
                if current_location.objects_present:
                    return Decision(ActionType.INTERACT_WITH_ENVIRONMENT, 
                                  random.choice(current_location.objects_present),
                                  "Repairing what's broken")
            return Decision(ActionType.INTERACT_WITH_ANIMAL, 
                          character.animal_companion.name,
                          "Attending to the pigs while birds circle overhead")
        
        # The One Who Knows
        elif character.id == "knows_too_much":
            if other_characters_present:
                # Make meta-comments about simulation
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Referencing simulation parameters as if they're weather")
            return Decision(ActionType.INTERACT_WITH_ANIMAL,
                          "the horse-motorcycle",
                          "Adjusting the form that won't stay stable")
        
        # Forget-Nothing  
        elif character.id == "forget_nothing":
            if "repair" in driver.lower() or "work" in driver.lower():
                if current_location.objects_present:
                    return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                                  current_location.objects_present[0],
                                  "Working—mechanic, blacksmith, whatever is needed")
            return Decision(ActionType.OBSERVE, None, "Remembering this moment with all the others")
        
        # Parade
        elif character.id == "parade":
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Drawing into ceremony")
            return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                          random.choice(current_location.objects_present) if current_location.objects_present else "space",
                          "Creating parade from nothing")
        
        # Measurer
        elif character.id == "measurer":
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Measuring the distance between them mid-conversation")
            return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                          random.choice(current_location.objects_present) if current_location.objects_present else "gaps",
                          "Measuring gaps, objects, silence duration")
        
        # Tuesday (only active on Tuesdays in simulation)
        elif character.id == "tuesday":
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Smiling when asked about the suitcase")
            return Decision(ActionType.INTERACT_WITH_ANIMAL,
                          "Seven",
                          "Standing near the pig that knows the secret")
        
        # Backward Walker
        elif character.id == "backward":
            # Always backing away even when interacting
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Conversing while backing away")
            return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                          random.choice(current_location.objects_present) if current_location.objects_present else "space",
                          "Repairing while walking backward from it")
        
        # Collector
        elif character.id == "collector":
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Picking up dropped words from conversation")
            return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                          "fallen things",
                          "Collecting what has fallen, filling pockets")
        
        # The Listener
        elif character.id == "listener":
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_CHARACTER,
                              other_characters_present[0].id,
                              "Responding to something they didn't say")
            return Decision(ActionType.OBSERVE, None,
                          "Hearing what the silence sounds like")
        
        # Sleeper
        elif character.id == "sleeper":
            # Always sleeping, even when acting
            return Decision(ActionType.OBSERVE, None,
                          "Sleeping standing, eyes open, seeing dream-truths")
        
        # Default behavior
        return Decision(ActionType.OBSERVE, None, "Momentary pause")
    
    def _decide_rider(self, character: Character, driver: str, 
                     current_location: Location,
                     available_locations: Dict[str, Location],
                     other_characters_present: List[Character]) -> Decision:
        """Decision logic for The Rider."""
        
        if "control" in driver.lower():
            # Seek spaces where control can be exerted
            if current_location.id == "loc_courtyard":
                # Stay and interact with environment or horse
                if random.random() < 0.6:
                    return Decision(ActionType.INTERACT_WITH_ANIMAL, 
                                  character.animal_companion.name,
                                  "Asserting control over the horse")
            else:
                # Move to courtyard or parade ground
                if "loc_courtyard" in available_locations:
                    return Decision(ActionType.MOVE_TO_LOCATION, "loc_courtyard",
                                  "Seeking space for control")
        
        if "violence" in driver.lower():
            # Seek confrontational interactions
            if other_characters_present:
                target = random.choice(other_characters_present)
                return Decision(ActionType.INTERACT_WITH_CHARACTER, target.id,
                              "Testing boundaries through confrontation")
        
        if "connection" in driver.lower():
            # Conflicted - approach then withdraw
            if other_characters_present and character.id == "handler_01":
                return Decision(ActionType.OBSERVE, None,
                              "Watching others but unable to connect")
        
        # Default - interact with environment to assert presence
        if current_location.objects_present:
            obj = random.choice(current_location.objects_present)
            return Decision(ActionType.INTERACT_WITH_ENVIRONMENT, obj,
                          "Asserting presence through object manipulation")
        
        return Decision(ActionType.OBSERVE, None, "Tense observation")
    
    def _decide_handler(self, character: Character, driver: str,
                       current_location: Location,
                       available_locations: Dict[str, Location],
                       other_characters_present: List[Character]) -> Decision:
        """Decision logic for The Handler."""
        
        if "equilibrium" in driver.lower() or "protect" in driver.lower():
            # Seek animals or quiet spaces
            if current_location.id in ["loc_stable", "loc_water_station"]:
                # Stay and work with animals
                return Decision(ActionType.INTERACT_WITH_ANIMAL,
                              character.animal_companion.name,
                              "Maintaining balance through animal care")
            else:
                # Move to stable or workshop
                if "loc_stable" in available_locations:
                    return Decision(ActionType.MOVE_TO_LOCATION, "loc_stable",
                                  "Seeking animal space")
        
        if "avoidance" in driver.lower():
            # If crowded, leave
            if len(other_characters_present) > 2:
                # Move to solitary location
                solitary_locs = ["loc_workshop", "loc_stable", "loc_burial_ground"]
                available_solitary = [loc for loc in solitary_locs if loc in available_locations]
                if available_solitary:
                    return Decision(ActionType.MOVE_TO_LOCATION, random.choice(available_solitary),
                                  "Avoiding human unpredictability")
        
        if "ritual" in driver.lower():
            # Engage with environment in ordered way
            if current_location.objects_present:
                return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                              current_location.objects_present[0],
                              "Creating order through routine")
        
        return Decision(ActionType.OBSERVE, None, "Quiet observation")
    
    def _decide_drifter(self, character: Character, driver: str,
                       current_location: Location,
                       available_locations: Dict[str, Location],
                       other_characters_present: List[Character]) -> Decision:
        """Decision logic for The Drifter."""
        
        if "avoid being known" in driver.lower():
            # Always on the move
            if random.random() < 0.7:
                # Leave for another location
                possible = [loc for loc in available_locations.keys() 
                          if loc != current_location.id]
                if possible:
                    return Decision(ActionType.MOVE_TO_LOCATION, random.choice(possible),
                                  "Avoiding permanence")
        
        if "music" in driver.lower():
            # Observe then play music (represented as environment interaction)
            if other_characters_present:
                return Decision(ActionType.INTERACT_WITH_ENVIRONMENT, "harmonica",
                              "Communicating through music")
        
        if "witness" in driver.lower():
            # Observe without participating
            if other_characters_present:
                return Decision(ActionType.OBSERVE, None,
                              "Witnessing without consequence")
        
        # Drifter defaults to moving
        possible = [loc for loc in available_locations.keys() 
                   if loc != current_location.id]
        if possible:
            return Decision(ActionType.MOVE_TO_LOCATION, random.choice(possible),
                          "Compulsive movement")
        
        return Decision(ActionType.OBSERVE, None, "Brief pause before leaving")
    
    def _decide_witness(self, character: Character, driver: str,
                       current_location: Location,
                       available_locations: Dict[str, Location],
                       other_characters_present: List[Character]) -> Decision:
        """Decision logic for The Witness."""
        
        # The Witness almost always observes
        if "record" in driver.lower() or "document" in driver.lower():
            if other_characters_present:
                return Decision(ActionType.OBSERVE, None,
                              "Recording events in journal")
        
        if "patterns" in driver.lower():
            # Move to where action is likely
            activity_locs = ["loc_courtyard", "loc_bonfire", "loc_parade_ground", "loc_crossroads"]
            available_activity = [loc for loc in activity_locs if loc in available_locations]
            if available_activity and current_location.id not in activity_locs:
                return Decision(ActionType.MOVE_TO_LOCATION, random.choice(available_activity),
                              "Seeking patterns in active spaces")
        
        # The Witness rarely leaves unless to follow action
        return Decision(ActionType.OBSERVE, None, "Silent documentation")
    
    def _decide_celebrant(self, character: Character, driver: str,
                         current_location: Location,
                         available_locations: Dict[str, Location],
                         other_characters_present: List[Character]) -> Decision:
        """Decision logic for The Celebrant."""
        
        if "joy" in driver.lower() or "celebration" in driver.lower():
            # Seek gathering spaces
            if current_location.id == "loc_parade_ground":
                # Organize activity
                if other_characters_present:
                    return Decision(ActionType.INTERACT_WITH_CHARACTER,
                                  other_characters_present[0].id,
                                  "Drawing others into celebration")
                else:
                    # Prepare space
                    return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                                  "drums" if "drums" in current_location.objects_present else current_location.objects_present[0],
                                  "Preparing ritual space")
            else:
                # Move to parade ground or bonfire
                if "loc_parade_ground" in available_locations:
                    return Decision(ActionType.MOVE_TO_LOCATION, "loc_parade_ground",
                                  "Seeking performance space")
        
        if "essential" in driver.lower():
            # Must be where people are
            if not other_characters_present:
                # Find people
                return Decision(ActionType.MOVE_TO_LOCATION,
                              random.choice(list(available_locations.keys())),
                              "Seeking community to serve")
        
        if "beauty" in driver.lower():
            # Interact with environment to beautify
            if current_location.objects_present:
                return Decision(ActionType.INTERACT_WITH_ENVIRONMENT,
                              random.choice(current_location.objects_present),
                              "Creating beauty through decoration")
        
        return Decision(ActionType.INTERACT_WITH_ANIMAL, character.animal_companion.name,
                       "Decorating and preparing the horse")

