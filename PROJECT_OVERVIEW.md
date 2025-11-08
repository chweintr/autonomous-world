# Project Overview - Autonomous World System

## What Is This?

An autonomous character simulation system that generates vivid, painterly field notes for visual art production. Five characters with deep psychological profiles interact autonomously in a detailed environment, creating emergent narratives and charged moments that serve as source material for paintings.

## Quick Facts

- **Characters**: 5 unique archetypes with animal companions
- **Locations**: 12 atmospheric spaces (desert, courtyard, stable, etc.)
- **Output**: Vivid field notes with visual details and emotional temperature
- **Interface**: Web-based + command-line
- **Autonomy**: Characters make their own decisions based on psychological drivers
- **Emergence**: Patterns and unexpected behaviors tracked automatically
- **LLM Support**: Optional integration with GPT-4/Claude for enhanced descriptions
- **Scalable**: Designed to evolve from text → 2D images → AR → 3D spatial

## Key Features

### ✓ Autonomous Behavior
Characters act based on motivational drivers, not scripts. Add 20-30% randomness for unexpected moments.

### ✓ Animal Psychology
Each character has an animal companion that externalizes their suppressed impulses:
- Rider's horse shows his hidden vulnerability
- Handler's pigs show her anxiety
- Drifter's wolves show their abandoned rage
- Witness's crow shows their suppressed voice
- Celebrant's horse shows her exhaustion

### ✓ Rich Environment
12 distinct locations with properties like lighting quality, temperature, acoustics, and atmosphere. Time of day affects behavior.

### ✓ Painterly Output
Field notes focus on observable phenomena:
- Physical gestures and spatial relationships
- Color, light, and material details
- Emotional charge visible in body language
- What an artist would see

### ✓ Emergence Tracking
System identifies patterns automatically:
- Character location preferences
- Recurring character pairings
- Location emotional atmospheres
- Unexpected/emergent moments

### ✓ Full Control
Adjust autonomy, randomness, interaction density, and duration to shape the simulation.

## File Structure

```
autonomous-world/
├── README.md              # Full documentation
├── QUICKSTART.md          # Get running in 5 minutes
├── USAGE_GUIDE.md         # Scenario design & tips
├── TECHNICAL.md           # Architecture & API reference
├── run.py                 # Start web interface
├── example_scenario.py    # Command-line example
├── requirements.txt       # Dependencies
│
├── data/
│   ├── characters/        # 5 character JSON files
│   ├── locations/         # 12 location JSON files
│   └── sessions/          # Saved field notes (generated)
│
├── src/
│   ├── models/            # Character, Location, Interaction
│   ├── engine/            # World state, decision engine, simulation
│   ├── generators/        # LLM-based description generation
│   ├── utils/             # Configuration loader
│   └── api/               # Flask web API
│
├── web/
│   ├── templates/         # HTML interface
│   └── static/            # CSS & JavaScript
│
└── config/
    └── default_config.json
```

## The Characters

1. **Marcus Vale - The Rider**: Former cavalry, leopard-print jacket, commands his horse Redline who shows his suppressed vulnerability

2. **Iris Kahn - The Handler**: Animal trainer, embroidered vest, works with three pigs (Bracket, Spindle, Moth) who externalize her anxiety

3. **The Drifter (Stripe)**: Gender-ambiguous wanderer, striped clothing, plays harmonica, shadowed by wolves representing abandoned rage

4. **The Witness**: Masked silent observer with journal, accompanied by crow Augur who externalizes their suppressed voice

5. **Solene Marche - The Celebrant**: Parade organizer, bright colors, rides painted horse Reverie who shows her hidden exhaustion

## How It Works

1. **Seed Scenario**: Place characters in locations
2. **Set Parameters**: Autonomy, randomness, density, duration
3. **Run Simulation**: Characters make autonomous decisions
4. **Generate Field Notes**: Each interaction produces vivid description
5. **Track Emergence**: Patterns identified automatically
6. **Save Session**: Export field notes as markdown

Each simulation run is unique due to randomness and autonomous decision-making.

## Example Output

```
[18:47 - Courtyard - Dusk]
The rider in the leopard-print jacket leans into the horse's neck. 
His hands grip too tight. The horse's ears flatten. A pink pig 
circles them twice, then stops at the rider's feet. The sky behind 
them is bakery pink turning to midnight blue. A white rope lies 
coiled near the archway.

Material details: Leopard print against chestnut coat. Pink pig, 
pink sky. White rope on cracked concrete. Harsh shadows lengthening.

Emotional temperature: Tense, verging on rupture
```

## Getting Started

### Fastest Path (Web Interface)

```bash
pip install -r requirements.txt
python run.py
# Open http://localhost:5000
```

### Command Line Example

```bash
python example_scenario.py
```

### Learn More

- **New user?** Read [QUICKSTART.md](QUICKSTART.md)
- **Want to create scenarios?** Read [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Need full details?** Read [README.md](README.md)
- **Developer?** Read [TECHNICAL.md](TECHNICAL.md)

## Use Cases

### For Visual Artists
- Generate source material for paintings
- Explore character psychology through observation
- Create series based on recurring patterns
- Use field notes as compositional sketches

### For Writers
- Character development through autonomous behavior
- World-building with emergent narratives
- Psychological exploration via animal companions
- Source material for experimental fiction

### For Game Designers
- Prototype autonomous NPC behavior
- Test character motivation systems
- Develop emergent narrative mechanics
- Explore animal companion dynamics

### For Researchers
- Study emergent behavior in simulations
- Experiment with decision-making models
- Test pattern recognition systems
- Develop autonomous character frameworks

## Design Principles

1. **Autonomy over scripting**: Characters decide, don't follow scripts
2. **Emergence over planning**: Best moments arise unexpectedly
3. **Observable over internal**: Focus on what can be seen
4. **Painterly over literary**: Visual details, not metaphors
5. **Modular over monolithic**: Easy to extend and scale

## Future Roadmap

- **Phase 2 (6mo)**: 2D image generation for key moments
- **Phase 3 (12mo)**: AR placement and spatial observation
- **Phase 4 (18mo)**: Full 3D spatial simulation with VR

System architecture designed to support this evolution.

## Success Criteria

The system succeeds when:

1. ✓ Characters behave in ways you didn't script
2. ✓ Animal behaviors feel psychologically true
3. ✓ Field notes provide compelling painting source material
4. ✓ You can "enter" the world, observe, and return with ideas
5. ✓ System scales gracefully as better AI tools emerge

## Status: Phase 1 Complete

**Phase 1** (Text-based simulation with LLM-generated descriptions) is **COMPLETE** and ready to use.

The system is fully functional, documented, and ready for:
- Art production
- Creative exploration
- Further development
- Scaling to visual and spatial modes

---

**Build. Observe. Create.**


