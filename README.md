# Autonomous World System

A text-based autonomous character simulation system designed as a generative engine for visual art production. Characters with rich psychological profiles interact autonomously in a detailed environment, generating vivid field notes that serve as source material for paintings and other visual art.

> **🚀 NEW USER? Start with [START_HERE.md](START_HERE.md) for quick answers**  
> **📖 Full roadmap: [CURRENT_STATE.md](CURRENT_STATE.md) → [PHASE_2_VISUAL.md](PHASE_2_VISUAL.md) → [FUTURE_ROADMAP.md](FUTURE_ROADMAP.md)**

## Overview

This system simulates a world of 5 persistent characters, each with their own motivations, relationships, and animal companions. Characters make autonomous decisions based on their psychological drivers, creating emergent narratives and charged moments. The system produces detailed field notes in a painterly style, documenting interactions with attention to gesture, space, light, and emotional temperature.

### Key Features

- **Autonomous Character Behavior**: Characters make decisions based on motivational drivers, not scripted sequences
- **Animal Companions**: Each character has an animal that externalizes their suppressed impulses
- **Rich Environmental System**: 12 distinct locations with atmospheric properties
- **Emergent Patterns**: Tracks and identifies patterns that arise from character interactions
- **Vivid Field Notes**: Generates painterly descriptions with material details and emotional temperature
- **LLM Integration**: Optional integration with GPT-4/Claude for enhanced descriptions
- **Web Interface**: User-friendly interface for seeding scenarios and viewing results
- **Modular Architecture**: Designed to scale from text to 3D spatial computing

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this directory

2. Install dependencies:
```bash
cd autonomous-world
pip install -r requirements.txt
```

3. (Optional) Set up LLM integration:
   - For OpenAI: Set environment variable `OPENAI_API_KEY`
   - Uncomment the appropriate line in `requirements.txt` and reinstall
   - Enable LLM in the web interface or `config/default_config.json`

4. Run the system:
```bash
python run.py
```

5. Open your browser to `http://localhost:5000`

## Quick Start

### Using the Web Interface

1. **Seed a Scenario**: 
   - Select locations for one or more characters
   - Click "Seed Scenario"

2. **Adjust Parameters**:
   - **Autonomy Level**: How much characters follow their drivers (0-1)
   - **Randomness**: Unpredictability in decisions (0-1, suggested: 0.2-0.3)
   - **Interaction Density**: Sparse/Moderate/Dense - how often actions occur
   - **Duration**: How long to run the simulation (in simulated minutes)

3. **Run Simulation**:
   - Click "Run Simulation"
   - Watch field notes appear in real-time

4. **Review Patterns**:
   - Click "Generate Report" to see emergent behaviors
   - Look for recurring character pairings, location preferences, unexpected moments

5. **Save Session**:
   - Click "Save Session" to export field notes as markdown

### Example Scenario

Try this to start:
- Place **Marcus Vale (The Rider)** at **The Courtyard**
- Place **Iris Kahn (The Handler)** at **Stable Ruin**
- Place **The Witness** at **The Rooftop**
- Set duration to 60 minutes
- Run simulation

The Rider will likely interact tensely with his horse. The Handler will work with her pigs. The Witness will observe. Characters may move between locations and interact.

## Characters

### The Rider - Marcus Vale
Former cavalry officer, now biker. Leopard-print jacket. Commands but doesn't control his chestnut horse **Redline**, who externalizes his suppressed vulnerability.

**Drivers**: Control, violence, freedom from past, hidden need for connection

### The Handler - Iris Kahn
Animal trainer. Embroidered vest. Works with three pigs (**Bracket, Spindle, Moth**) who externalize her hypervigilance and anxiety.

**Drivers**: Equilibrium through animal work, protection, avoidance of human unpredictability

### The Drifter (Stripe)
Gender-ambiguous, ageless. Striped clothing. Plays harmonica. Shadowed by wolves who represent their abandoned rage and pack loyalty.

**Drivers**: Avoid being known, witness without consequence, communicate through music

### The Witness
Masked face, silent observer. Carries journal. Accompanied by crow **Augur** who externalizes their suppressed voice.

**Drivers**: Document everything, remain separate, see patterns, protect through witnessing

### The Celebrant - Solene Marche
Organizer of parades and rituals. Bright colors, decorated horse **Reverie** who externalizes her exhaustion under constant performance.

**Drivers**: Create joy through ritual, mask despair with celebration, be essential

## Locations

The world contains 12 locations, each with distinct properties:

- **The Courtyard**: Confrontational walled space
- **Bonfire Site**: Ceremonial gathering place
- **The Patterned Room**: Hypnotic interior with geometric patterns
- **Parade Ground**: Exposed performative space
- **Stable Ruin**: Haunted by former purpose
- **Desert Clearing**: Austere and honest
- **The Rooftop**: Solitary observational perch
- **The Crossroads**: Liminal decision point
- **Water Station**: Necessary communal space
- **Canyon Mouth**: Ancient and resonant
- **The Workshop**: Productive and contained
- **Burial Ground**: Peaceful and solemn

## Field Note Format

Field notes follow this structure:

```
[HH:MM - Location Name - Time of Day]
Action description (2-3 sentences): Vivid, specific physical details, gestures, spatial relationships.

Material details: Colors, textures, lighting, what would be visible.
Emotional temperature: Tense/Exuberant/Uncertain/Charged/etc.
```

### Example

```
[18:47 - Courtyard - Dusk]
The rider in the leopard-print jacket leans into the horse's neck. His hands grip too tight. The horse's ears flatten. A pink pig circles them twice, then stops at the rider's feet. The sky behind them is bakery pink turning to midnight blue. A white rope lies coiled near the archway.

Material details: Leopard print against chestnut coat. Pink pig, pink sky. White rope on cracked concrete.
Emotional temperature: Tense, verging on rupture
```

## Configuration

Edit `config/default_config.json` to adjust defaults:

```json
{
  "simulation": {
    "autonomy_level": 0.75,      // 0-1, character autonomy
    "randomness": 0.25,           // 0-1, unpredictability
    "interaction_density": "moderate",  // sparse/moderate/dense
    "time_compression": 60        // real minutes to sim minutes
  },
  "llm": {
    "enabled": false,             // Use LLM for descriptions
    "provider": "openai",         // openai/anthropic/ollama
    "model": "gpt-4"
  }
}
```

## Project Structure

```
autonomous-world/
├── data/
│   ├── characters/          # Character JSON files
│   ├── locations/           # Location JSON files
│   └── sessions/            # Saved field notes
├── src/
│   ├── models/              # Data models
│   │   ├── character.py
│   │   ├── location.py
│   │   └── interaction.py
│   ├── engine/              # Simulation engine
│   │   ├── world_state.py
│   │   ├── decision_engine.py
│   │   └── simulation.py
│   ├── generators/          # Description generators
│   │   └── description_generator.py
│   ├── utils/               # Utilities
│   │   └── config_loader.py
│   └── api/                 # Web API
│       └── app.py
├── web/
│   ├── templates/           # HTML templates
│   └── static/              # CSS/JS
├── config/
│   └── default_config.json
├── run.py                   # Main entry point
├── requirements.txt
└── README.md
```

## Advanced Usage

### Creating New Characters

1. Create a JSON file in `data/characters/`:

```json
{
  "id": "new_char_01",
  "name": "Character Name",
  "archetype": "The Archetype",
  "physical_description": "Detailed visual description...",
  "backstory": "200-300 word backstory...",
  "motivational_drivers": [
    "Driver 1",
    "Driver 2",
    "Driver 3"
  ],
  "relationships": {
    "rider_01": "Relationship description"
  },
  "animal_companion": {
    "species": "species",
    "name": "Name",
    "description": "Physical description",
    "externalized_impulse": "What suppressed aspect this represents",
    "temperament": "calm/aggressive/etc",
    "current_state": "neutral"
  },
  "emotional_state": "calm",
  "current_location": null,
  "emotional_intensity": 0.5
}
```

2. Add decision logic in `src/engine/decision_engine.py` for character-specific behavior

### Creating New Locations

Create a JSON file in `data/locations/`:

```json
{
  "id": "loc_new",
  "name": "Location Name",
  "description": "General description",
  "lighting_quality": "How light behaves",
  "temperature_range": "Hot/cool/varying",
  "acoustic_quality": "Echo/muffled/resonant",
  "objects_present": ["object1", "object2"],
  "architectural_features": ["feature1", "feature2"],
  "atmosphere": "Overall mood",
  "current_time": "midday",
  "current_weather": "clear"
}
```

### LLM Integration

To enable higher-quality descriptions:

1. Install LLM provider:
```bash
pip install openai  # or anthropic, or ollama
```

2. Set API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

3. Enable in config or web interface

The system will fall back to template-based generation if LLM fails.

## Emergence Tracking

The system automatically tracks:

- **Location Preferences**: Which characters gravitate to which spaces
- **Character Pairings**: Who interacts with whom repeatedly
- **Location Atmospheres**: Which emotional temperatures dominate each space
- **Unexpected Events**: Moments flagged as emergent behavior

Access reports via "Generate Report" in the web interface.

## Future Development Roadmap

### Phase 2 (6 months): Visual Generation
- Integration with Stable Diffusion or Midjourney for key moment visualization
- Character and location visual references
- Automatic image generation from field notes

### Phase 3 (12 months): AR Integration
- Integration with AR frameworks (8th Wall, ARCore)
- Spatial positioning data for characters
- Virtual observation within the world

### Phase 4 (18 months): Full 3D Simulation
- Real-time 3D character movement
- VR observation capabilities
- Integration with spatial computing platforms

## Design Philosophy

### Autonomy Over Scripting

Characters make decisions based on:
1. Their motivational drivers (primary influence)
2. Current emotional state
3. Environmental context
4. Presence of other characters
5. Randomness (20-30% unpredictability)

No two simulation runs will be identical.

### Animals as Externalized Psychology

Each animal companion represents what the character suppresses:
- The Rider's horse shows his hidden vulnerability
- The Handler's pigs show her anxiety
- The Drifter's wolves show their abandoned rage
- The Witness's crow shows their suppressed voice
- The Celebrant's horse shows her exhaustion

Animals behave semi-independently, creating moments of psychological revelation.

### Painterly Description

All descriptions focus on what would be **visible**:
- Physical gestures and postures
- Spatial relationships
- Color and light
- Material textures
- Body language

No metaphors or internal states—only observable phenomena.

## Troubleshooting

### "No module named 'src'"
- Make sure you're running from the `autonomous-world` directory
- Run: `python run.py` not `python src/api/app.py`

### LLM Not Working
- Check API key is set: `echo $OPENAI_API_KEY`
- Verify package installed: `pip show openai`
- Check console for error messages
- System will fall back to templates if LLM fails

### No Interactions Generated
- Ensure characters are placed in locations (seed scenario first)
- Try increasing duration or interaction density
- Check that at least one character is placed

### Field Notes Too Generic
- Enable LLM integration for more specific descriptions
- Increase randomness for more unexpected moments
- Try different character combinations

## Contributing

To extend the system:

1. **Add Characters**: Create JSON in `data/characters/`, add decision logic
2. **Add Locations**: Create JSON in `data/locations/`
3. **Enhance Descriptions**: Modify `description_generator.py` templates or prompts
4. **New Interaction Types**: Extend `InteractionType` enum and handlers
5. **Better Decision Making**: Refine logic in `decision_engine.py`

## License

This project is provided as-is for creative and artistic purposes.

## Credits

Created as a generative engine for visual art production, inspired by the intersection of autonomous systems, psychological archetypes, and painterly observation.

---

**Built with maximum modularity. Phase 1 complete. Ready to scale.**

