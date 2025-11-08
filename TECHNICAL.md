# Technical Documentation - Autonomous World System

## Architecture Overview

The system is built with modularity and extensibility in mind, designed to scale from text-based simulation to 3D spatial computing.

### Core Components

```
┌─────────────────┐
│  Web Interface  │  (Flask + JavaScript)
└────────┬────────┘
         │
┌────────▼────────┐
│   API Layer     │  (Flask routes)
└────────┬────────┘
         │
┌────────▼────────┐
│   Simulation    │  (Orchestration)
│     Engine      │
└────┬────────┬───┘
     │        │
┌────▼───┐ ┌─▼──────────┐
│Decision│ │Description │
│Engine  │ │Generator   │
└────┬───┘ └─┬──────────┘
     │       │
┌────▼───────▼───┐
│  World State   │
│   Management   │
└────────┬───────┘
         │
┌────────▼────────┐
│  Data Models    │  (Character, Location, Interaction)
└─────────────────┘
```

## Data Models

### Character Model

**File**: `src/models/character.py`

```python
@dataclass
class Character:
    id: str
    name: str
    archetype: str
    physical_description: str
    backstory: str
    motivational_drivers: List[str]
    relationships: Dict[str, str]
    animal_companion: Animal
    emotional_state: EmotionalState
    current_location: Optional[str]
    emotional_intensity: float
```

**Key Methods**:
- `shift_emotional_state(new_state, intensity_delta)`: Update character state
- `get_dominant_driver()`: Get current motivational driver
- `save_to_file(filepath)`: Serialize to JSON
- `load_from_file(filepath)`: Deserialize from JSON

### Location Model

**File**: `src/models/location.py`

```python
@dataclass
class Location:
    id: str
    name: str
    description: str
    lighting_quality: str
    temperature_range: str
    acoustic_quality: str
    objects_present: List[str]
    architectural_features: List[str]
    atmosphere: str
    current_time: TimeOfDay
    current_weather: Weather
```

**Key Methods**:
- `get_environmental_description()`: Get current conditions description

### Interaction Model

**File**: `src/models/interaction.py`

```python
@dataclass
class Interaction:
    timestamp: datetime
    location_id: str
    location_name: str
    interaction_type: InteractionType
    characters_present: List[str]
    animals_present: List[str]
    action_description: str
    material_details: str
    emotional_temperature: EmotionalTemperature
    time_of_day: str
    weather: str
    environmental_context: str
    is_unexpected: bool
    pattern_tags: List[str]
```

**Key Methods**:
- `to_field_note()`: Format as markdown field note
- `to_dict()`: Serialize to dictionary

## Simulation Engine

### World State

**File**: `src/engine/world_state.py`

Manages the current state of the simulation world.

**Key Methods**:
```python
advance_time(minutes)                    # Move time forward
get_characters_at_location(location_id)  # Get characters at a location
add_interaction(interaction)             # Log an interaction
save_session(session_name, output_dir)   # Export field notes
```

**Time Management**:
- Tracks simulation time independently of real time
- Time compression configurable (default: 1 real min = 60 sim mins)
- Automatically updates environmental conditions (time of day)

### Decision Engine

**File**: `src/engine/decision_engine.py`

Makes autonomous decisions for characters based on their drivers and context.

**Decision Process**:
1. Check randomness threshold → random action if triggered
2. Get character's dominant driver
3. Apply character-specific decision logic
4. Consider environmental context
5. Evaluate presence of other characters
6. Return `Decision` object

**Decision Types**:
```python
class ActionType(Enum):
    MOVE_TO_LOCATION
    INTERACT_WITH_CHARACTER
    INTERACT_WITH_ANIMAL
    INTERACT_WITH_ENVIRONMENT
    OBSERVE
    LEAVE
```

**Character-Specific Logic**:

Each character has unique decision patterns:

- **Rider**: Seeks control spaces, tests boundaries, conflicted about connection
- **Handler**: Seeks animals/quiet, avoids crowds, creates routine
- **Drifter**: Always moving, communicates through music, witnesses without participation
- **Witness**: Observes, seeks active spaces to document, rarely acts
- **Celebrant**: Seeks gathering spaces, creates celebration, needs to be central

### Simulation Controller

**File**: `src/engine/simulation.py`

Orchestrates the entire simulation.

**Main Loop**:
```python
while elapsed < duration:
    1. Select active character
    2. Get current context (location, other characters)
    3. Decide action (via DecisionEngine)
    4. Execute decision
    5. Generate description (via DescriptionGenerator)
    6. Create Interaction
    7. Update character state
    8. Track for emergence
    9. Advance time
```

**Configuration**:
```python
class SimulationConfig:
    autonomy_level: float       # How much characters follow drivers
    time_compression: int       # Real to sim time ratio
    interaction_density: str    # sparse/moderate/dense
    narrative_coherence: str    # loose/tight
    randomness: float          # Unpredictability factor
```

## Description Generation

### LLM Integration

**File**: `src/generators/description_generator.py`

Generates vivid descriptions either via LLM or templates.

**LLM Mode**:
1. Build context prompt with character, location, action data
2. Call LLM API (OpenAI, Anthropic, or Ollama)
3. Parse JSON response
4. Extract action, material details, emotional temperature
5. Fall back to templates on error

**Template Mode**:
- Uses pre-written templates with variable insertion
- Randomizes language to avoid repetition
- Faster and free, but less specific

**System Prompt** (for LLM):
```
You are a visual artist creating field notes for paintings.
Focus on:
- Physical gestures and postures
- Spatial relationships
- Color and light quality
- Material textures
- Emotional charge in body language
- What would be visible

Write in present tense with concrete details.
No metaphors - only observable phenomena.
```

## Emergence Tracking

**File**: `src/engine/simulation.py` (`EmergenceTracker` class)

Tracks patterns automatically during simulation.

**Tracked Metrics**:

1. **Location Preferences**: `Dict[character_id, Dict[location_id, visit_count]]`
2. **Character Pairings**: `Dict[tuple, interaction_count]`
3. **Location Atmospheres**: `Dict[location_id, List[EmotionalTemperature]]`
4. **Unexpected Events**: `List[Interaction]` (where `is_unexpected=True`)

**Pattern Detection**:
- Identifies favorite locations (most visits)
- Finds significant pairings (3+ interactions)
- Calculates dominant atmosphere per location
- Collects emergent moments

**Report Generation**:
```python
generate_report() -> str  # Markdown report
```

## API Endpoints

### Character & Location Data

```
GET  /api/characters          # List all characters
GET  /api/locations           # List all locations
```

### Simulation Control

```
POST /api/scenario/seed       # Place characters, initialize simulation
POST /api/simulation/run      # Run simulation for duration
GET  /api/simulation/status   # Get current status
POST /api/reset               # Reset simulation
```

### Data Retrieval

```
GET  /api/interactions/recent # Get recent interactions
GET  /api/emergence/report    # Get emergence patterns
POST /api/session/save        # Save session as markdown
```

### Example: Seed Scenario

**Request**:
```json
POST /api/scenario/seed
{
  "placements": {
    "rider_01": "loc_courtyard",
    "handler_01": "loc_stable"
  },
  "config": {
    "autonomy_level": 0.75,
    "randomness": 0.25,
    "interaction_density": "moderate"
  },
  "use_llm": false
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Scenario seeded with 2 characters"
}
```

### Example: Run Simulation

**Request**:
```json
POST /api/simulation/run
{
  "duration_minutes": 60
}
```

**Response**:
```json
{
  "status": "success",
  "interactions_count": 12,
  "interactions": [...]
}
```

## Configuration System

**File**: `src/utils/config_loader.py`

Loads and manages configuration from JSON files.

**Usage**:
```python
from src.utils.config_loader import ConfigLoader

config = ConfigLoader('config/default_config.json')

# Get values with dot notation
autonomy = config.get('simulation.autonomy_level')  # 0.75
model = config.get('llm.model')  # "gpt-4"

# Set values
config.set('simulation.randomness', 0.3)

# Save changes
config.save()
```

## Extending the System

### Adding a New Character

1. **Create JSON** in `data/characters/`:
   - Define all required fields
   - Create unique `id`
   - Design animal companion (what do they suppress?)

2. **Add Decision Logic** in `src/engine/decision_engine.py`:
   ```python
   def _decide_new_character(self, character, driver, ...):
       if "some_driver" in driver.lower():
           # Decision logic here
           return Decision(...)
   ```

3. **Add to main decision router**:
   ```python
   elif character.id == "new_char_01":
       return self._decide_new_character(...)
   ```

### Adding a New Location

1. **Create JSON** in `data/locations/`:
   - Define atmospheric properties
   - List objects and architectural features
   - Consider how lighting/acoustics affect interactions

2. **Optional**: Add location-specific behavior in `decision_engine.py`:
   ```python
   if current_location.id == "loc_new":
       # Special behavior in this location
   ```

### Adding New Interaction Types

1. **Extend Enum** in `src/models/interaction.py`:
   ```python
   class InteractionType(Enum):
       ...
       NEW_TYPE = "new_type"
   ```

2. **Handle in Simulation** in `src/engine/simulation.py`:
   ```python
   elif decision.action_type == ActionType.NEW_TYPE:
       interaction_type = InteractionType.NEW_TYPE
       # Additional logic
   ```

3. **Update Description Generator** to handle new type

### Customizing LLM Prompts

Edit `src/generators/description_generator.py`:

**System Prompt**: `_get_system_prompt()`
**User Prompt**: `_build_prompt()`

Adjust for:
- Different artistic styles
- More/less detail
- Specific visual focus (color, gesture, space)
- Output format

### Adding New LLM Providers

1. **Install provider library**:
   ```bash
   pip install anthropic  # or ollama, etc.
   ```

2. **Add provider logic** in `description_generator.py`:
   ```python
   if self.provider == "anthropic":
       # Anthropic API call
   elif self.provider == "ollama":
       # Ollama local model call
   ```

3. **Update config**:
   ```json
   "llm": {
     "provider": "anthropic",
     "model": "claude-3-opus"
   }
   ```

## Performance Considerations

### Optimization Points

1. **LLM Calls**: Most expensive operation
   - Cache frequent scenarios
   - Use templates for iteration
   - Batch requests if possible

2. **File I/O**: Loading characters/locations
   - Cached in WorldState after first load
   - Only reload on reset

3. **Simulation Speed**:
   - Interaction density controls cycle frequency
   - Time compression affects real-time duration
   - Background execution possible

### Scaling

**Current Capacity**:
- 5-10 characters: Smooth
- 10-15 locations: Smooth
- 1000+ interactions per session: Smooth

**Future Optimization**:
- Database storage for large session histories
- Async LLM calls
- Parallel character decision-making
- Caching for common decisions

## Testing

### Unit Testing (Future)

Recommended test coverage:

```python
# Character tests
test_character_serialization()
test_emotional_state_shifts()
test_driver_selection()

# Location tests
test_location_environmental_updates()
test_time_of_day_transitions()

# Decision engine tests
test_decision_based_on_driver()
test_randomness_threshold()
test_character_specific_logic()

# Simulation tests
test_simulation_time_advancement()
test_interaction_generation()
test_character_state_updates()
```

### Integration Testing

Test scenarios:
1. Full simulation run with all characters
2. LLM integration (with mock API)
3. Session save/load
4. Emergence tracking accuracy

## Future Architecture

### Phase 2: Visual Generation

**New Components**:
- Image generation integration (Stable Diffusion, Midjourney)
- Visual cache for characters/locations
- Image-to-image transformation based on field notes

**Data Model Extensions**:
```python
@dataclass
class Character:
    ...
    visual_reference: str  # Path to image
    model_3d: Optional[str]  # 3D model reference
```

### Phase 3: AR Integration

**New Components**:
- Spatial coordinate system
- AR framework connector (8th Wall, ARCore)
- Real-world mapping

**Data Model Extensions**:
```python
@dataclass
class Location:
    ...
    coordinates: Tuple[float, float, float]  # 3D position
    ar_anchor: Optional[str]  # AR anchor ID
```

### Phase 4: 3D Spatial Computing

**New Components**:
- Real-time 3D renderer
- Character animation system
- VR observation mode
- Spatial audio

**Full 3D Engine**:
- Replace text simulation with spatial simulation
- Characters move in 3D space
- Field notes generated from observation position
- First-person exploration mode

---

## Debugging

### Enable Debug Mode

```python
# In run.py or config
app.run(debug=True)
```

### Common Debug Points

**Character not acting as expected**:
- Check `decision_engine.py` logic for that character
- Print driver and context in decision method
- Verify emotional state updates

**Interactions too generic**:
- Check if LLM is enabled and working
- Verify API key set correctly
- Review template variety in `description_generator.py`

**Emergence patterns not appearing**:
- Run longer simulations (120+ minutes)
- Ensure multiple characters interacting
- Check tracking in `EmergenceTracker`

### Logging

Add logging throughout:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug(f"Character {char.name} decided: {decision.reasoning}")
```

---

**System designed for extensibility. All components can be replaced or enhanced independently.**


