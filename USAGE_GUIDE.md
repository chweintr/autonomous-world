# Usage Guide - Autonomous World System

This guide provides practical instructions for using the system to generate compelling field notes for visual art.

## Getting Started

### First Run

1. Start the system:
```bash
cd autonomous-world
python run.py
```

2. Open browser to `http://localhost:5000`

3. You'll see three panels:
   - **Control Panel** (left): Set up and run simulations
   - **Field Notes** (top right): View generated interactions
   - **Emergence Patterns** (bottom right): See patterns emerge

## Creating Compelling Scenarios

### Scenario Design Principles

**1. Tension Through Pairing**

Place characters with conflicting drivers together:
- **Marcus (Rider) + Iris (Handler)** at Courtyard: His need for control vs. her need for calm
- **Solene (Celebrant) + Drifter** at Parade Ground: Her need to hold vs. their need to leave
- **Marcus + Solene** anywhere: Rigidity vs. exuberance

**2. Character Isolation**

Place a character alone to see their relationship with their animal:
- **Marcus alone** at Desert Clearing: Pure interaction with Redline's fear
- **Iris alone** at Workshop: Ritual behavior with the pigs
- **Witness alone** at Rooftop: Observation itself becomes the event

**3. Charged Locations**

Some locations inherently create tension:
- **Courtyard**: Forces proximity, confrontational
- **Water Station**: Forces cooperation
- **Crossroads**: Emphasizes choice and transition
- **Burial Ground**: Brings out melancholy

**4. Ritual Spaces**

Some locations encourage ceremonial behavior:
- **Bonfire Site**: Natural gathering, ritual fire
- **Parade Ground**: Performance and spectacle
- **Patterned Room**: Hypnotic, disorienting
- **Canyon Mouth**: Ancient, echoing

### Example Scenarios

#### Scenario 1: "Rupture at the Courtyard"
```
Marcus (Rider) → Courtyard
Iris (Handler) → Courtyard
Witness → Rooftop (to observe)

Duration: 30-60 minutes
Density: Moderate
Randomness: 0.3

Expected outcome: Marcus's control issues clash with Iris's need for calm. 
Horses and pigs create animal-to-animal tension. Witness documents.
```

#### Scenario 2: "Parade of One"
```
Solene (Celebrant) → Parade Ground
Drifter → Parade Ground (arrives, observes, leaves)

Duration: 90 minutes
Density: Sparse
Randomness: 0.25

Expected outcome: Solene prepares a parade alone. Drifter appears, refuses 
to join, plays harmonica, vanishes. Solene's desperation shows through Reverie.
```

#### Scenario 3: "Water Convergence"
```
ALL characters → Water Station

Duration: 45 minutes
Density: Dense
Randomness: 0.4

Expected outcome: Everyone needs water. Forced proximity. Animals compete. 
Unexpected alliances or conflicts. High emergence potential.
```

#### Scenario 4: "Isolation Studies"
```
Marcus → Desert Clearing
Iris → Workshop
Drifter → Crossroads
Witness → Burial Ground
Solene → Bonfire Site (preparing alone)

Duration: 120 minutes
Density: Sparse
Randomness: 0.2

Expected outcome: Each character with their animal, no human interaction. 
Pure externalized psychology. Watch for characters to eventually seek each other.
```

## Adjusting Parameters

### Autonomy Level (0.0 - 1.0)

- **0.9-1.0**: Characters rigidly follow their drivers. Predictable, psychologically consistent.
- **0.7-0.8**: Balanced. Characters mostly follow drives with some flexibility.
- **0.5-0.6**: More unpredictable. Drivers guide but don't dominate.
- **0.0-0.4**: Chaotic. Drivers have minimal influence.

**Recommendation**: Start at 0.75. Lower for more surprise.

### Randomness (0.0 - 1.0)

- **0.1-0.2**: Characters behave logically. Few surprises.
- **0.25-0.3**: Sweet spot. Unexpected moments emerge naturally.
- **0.4-0.5**: Frequent unexpected behavior. High emergence.
- **0.6+**: Very chaotic. Characters act irrationally.

**Recommendation**: 0.25 for natural emergence. 0.4 for experimental runs.

### Interaction Density

- **Sparse**: Action every ~10 sim minutes. Slow, contemplative.
- **Moderate**: Action every ~5 sim minutes. Natural pace.
- **Dense**: Action every ~2 sim minutes. Intense, packed with events.

**Recommendation**: Moderate for most scenarios. Sparse for isolation studies.

### Duration

- **15-30 minutes**: Quick sketch. 3-6 interactions.
- **60 minutes**: Standard session. 10-15 interactions.
- **120+ minutes**: Extended observation. 20+ interactions. Patterns emerge.

**Recommendation**: 60 minutes for first runs. 120+ to see patterns.

## Reading Field Notes

### What to Look For

**Physical Arrangements**
- Who is close to whom
- Body postures (leaning, gripping, standing rigid)
- Spatial triangles (two humans, one animal)
- Objects that mediate interaction (rope, bottles, instruments)

**Color and Light**
- Time of day creating mood
- Colors that repeat or clash
- Shadows and how they fall
- Light quality (harsh, soft, striped)

**Emotional Charge**
- Tension in stillness
- Exuberance in movement
- Uncertainty in between-ness
- Charged moments where nothing happens but everything could

**Animal Behavior**
- When animals circle (anxiety)
- When animals flee (overwhelm)
- When animals approach (need)
- When animals mirror humans vs. contrast

### Paintable Moments

Look for notes with:
- Strong geometric arrangement (three figures, diagonal line, circle)
- Color contrast (leopard print + pink pig + white rope)
- Light drama (dusk, striped light through gaps, fire glow)
- Psychological visibility (hands gripping too tight, ears flattening)

Flag these for visual development.

## Using Emergence Reports

After running a simulation, click "Generate Report" to see:

### Location Tendencies

Which characters prefer which spaces:
- If Marcus gravitates to Courtyard repeatedly → his need for controlled confrontation
- If Iris avoids populated spaces → her avoidance intensifying
- If Drifter never settles → their compulsion confirmed

**Use this**: Future scenarios can either reinforce these (put them in preferred spaces) or challenge them (force them elsewhere).

### Recurring Pairings

Which characters repeatedly interact:
- Unexpected pairings (Witness + Drifter) suggest emergent relationship
- Avoided pairings (Marcus avoiding Celebrant) reveal tension
- Stable pairings (Iris + animals) confirm core behavior

**Use this**: Develop these relationships. Create scenarios forcing avoided pairings.

### Location Atmospheres

Which emotional temperatures dominate each space:
- Courtyard always "tense" → confirms design
- Workshop becomes "tender" → unexpected, explore this
- Bonfire shifts between "ritual" and "charged" → liminal space

**Use this**: Choose locations based on desired emotional outcome.

### Emergent Events

Moments flagged as unexpected:
- These are the gold. Unscripted moments where characters surprise you.
- Often the most paintable - they feel discovered, not constructed.

**Use this**: These are your source material. Build future scenarios around them.

## LLM Integration

### With LLM (GPT-4, Claude)

**Pros**:
- Highly specific, vivid descriptions
- Better spatial detail
- More varied language
- Painterly quality

**Cons**:
- Requires API key and costs money
- Slower generation
- May be overly literary at times

**When to use**: Final production runs, when you need maximum quality.

### Without LLM (Template-based)

**Pros**:
- Free, fast
- Still generates usable field notes
- More consistent format

**Cons**:
- Less specific detail
- More repetitive language
- Serviceable but not beautiful

**When to use**: Exploration, testing scenarios, quick iterations.

**Recommendation**: Start without LLM to explore system. Enable LLM for final runs you'll use for painting.

## Workflow for Artists

### 1. Exploration Phase (1-2 hours)

- Run 5-10 quick scenarios (30-60 min each)
- Try different character combinations
- Vary locations and parameters
- Don't use LLM yet (save costs)
- Note which scenarios feel promising

### 2. Refinement Phase (2-3 hours)

- Select 2-3 promising scenario types
- Run longer durations (90-120 min)
- Enable LLM
- Lower randomness slightly (0.2-0.25)
- Save these sessions

### 3. Pattern Analysis (1 hour)

- Generate emergence reports
- Identify recurring arrangements
- Note unexpected moments
- Find character pairings that create charge

### 4. Production Phase (Ongoing)

- Run targeted scenarios based on discoveries
- Use LLM for all production runs
- Adjust parameters to emphasize what works
- Save all sessions
- Build library of field notes

### 5. Visual Development

- Read field notes as you would field sketches
- Identify moments with strong:
  - Composition (spatial arrangement)
  - Color (described materials)
  - Gesture (body language)
  - Charge (emotional temperature)
- Use these as painting subjects

## Tips for Maximum Emergence

1. **Run Long**: 120+ minutes lets patterns develop
2. **Don't Over-Control**: Higher randomness = more surprises
3. **Force Proximity**: Water Station, Courtyard make interaction inevitable
4. **Watch Animals**: They reveal character psychology
5. **Note Silence**: "Nothing happens" can be charged
6. **Let Characters Move**: Don't lock them in place
7. **Read Between Events**: What's not said or done matters
8. **Trust the System**: Characters will surprise you

## Common Issues

### "Characters aren't doing anything interesting"

- Increase interaction density
- Place conflicting characters together
- Try charged locations (Courtyard, Water Station)
- Increase randomness to 0.35-0.4

### "Too chaotic, doesn't make sense"

- Lower randomness to 0.15-0.2
- Increase autonomy level to 0.85
- Use narrative coherence: tight (in config)
- Reduce interaction density

### "Same interactions repeating"

- Enable LLM for variation
- Try different character combinations
- Change time of day (affects location properties)
- Increase randomness

### "Animals not showing character psychology"

- Run longer scenarios (animals emerge over time)
- Isolate characters with their animals
- Watch for animal-to-animal interactions
- Read animal behavior as contrast to human behavior

## Advanced Techniques

### Time of Day Progression

Run multiple short scenarios at the same location through a day:
1. Dawn - sparse, isolated characters
2. Midday - dense, forced interaction
3. Dusk - moderate, drawing toward closure
4. Night - sparse, ritual behavior

### Character Arc Studies

Follow one character across locations:
1. Marcus at Courtyard (control)
2. Marcus at Desert Clearing (isolation)
3. Marcus at Burial Ground (confronting loss)
4. Marcus at Water Station (forced community)

### Ensemble Experiments

All characters, one location, extended time. Watch the space transform.

---

**Remember**: This is a generative tool. The system creates raw material. You select, interpret, and transform it into visual art. Trust the emergence, but curate ruthlessly.


