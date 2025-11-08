# Dialogue Visualization - Speech Bubbles + Spatial Map

## 💬 The Problem (Current)

**Field notes say:**
> "Words are exchanged between Witness and Measurer."

**But we need:**
> Witness: "The light is changing."  
> Measurer: "2.3 degrees warmer."

**Fixed in prompt** - LLM now MUST use actual quoted dialogue.

---

## 🗺️ Visual Enhancement (Phase 2 Feature)

### Concept: Spatial Dialogue View

**Instead of just text, show:**

```
┌─────────────────────────────────────┐
│     THE COURTYARD · NIGHT           │
├─────────────────────────────────────┤
│                                     │
│         [Witness]                   │
│        💬 "The light is             │
│           changing."                │
│                                     │
│              ↓ 2.3m                 │
│                                     │
│         [Measurer]                  │
│        💬 "2.3 degrees              │
│           warmer."                  │
│                                     │
│   🐦 Augur                          │
│                                     │
└─────────────────────────────────────┘
```

### Implementation:

**Phase 2a - Simple Version:**
- Parse dialogue from field notes
- Extract speaker + quote
- Display with avatars/icons
- Show spatial arrangement (who's where)

**Phase 2b - Interactive Map:**
- Top-down map of location
- Character icons positioned
- Speech bubbles appear
- Click to expand/hide

**Phase 3 - Animated:**
- Characters move on map
- Speech bubbles appear in sequence
- Spatial relationship visual

---

## 🎨 Avatar/Icon System

### Simple Icons (Phase 2a):

**Characters as colored circles with initials:**
- Witness: W (aqua circle)
- Measurer: M (pink circle)
- Collector: C (yellow circle)
- Etc.

**Or simple silhouettes:**
- Extract from your paintings
- Simplified black shapes
- Colored backgrounds

**Or emoji/symbols:**
- Witness: 👁️
- Measurer: 📏
- Collector: 🎒
- Bird Gatherer: 🕊️
- Etc.

### Phase 2b - Your Painted Avatars:

- Extract character faces/heads from your paintings
- Crop to circles
- Use as avatars
- Matches your aesthetic

---

## 💬 Speech Bubble Format

### Display Options:

**Option A: Comic-style bubbles**
```html
<div class="speech-bubble" data-character="witness">
  <span class="speaker">Witness</span>
  "The light is changing."
</div>
```

**Option B: Messenger-style**
```
Witness
┌─────────────────────┐
│ The light is        │
│ changing.           │
└─────────────────────┘

Measurer
┌─────────────────────┐
│ 2.3 degrees warmer. │
└─────────────────────┘
```

**Option C: Screenplay format**
```
WITNESS
  The light is changing.

MEASURER
  2.3 degrees warmer.
```

---

## 🗺️ Spatial Map Concept

### Top-Down Location View:

**The Courtyard:**
```
┌──────────────────────────┐
│ ╔════════════════╗       │ N
│ ║  [Archway]     ║       │ ↑
│ ║                ║       │
│ ║   👤 Witness   ║       │
│ ║   💬           ║       │
│ ║        ↓ 2.3m  ║       │
│ ║   👤 Measurer  ║       │
│ ║   💬           ║       │
│ ║                ║       │
│ ║  🐦 (bird)     ║       │
│ ║  🧵 (rope)     ║       │
│ ╚════════════════╝       │
└──────────────────────────┘
```

### Implementation:

**HTML Canvas or SVG:**
- Draw location outline
- Place character icons
- Position speech bubbles
- Show objects/props
- Indicate distances (Measurer would love this!)

**Interactive:**
- Click character → highlight their dialogue
- Hover bubble → show full field note
- Drag to rotate view (later)

---

## 🎬 Dialogue Timeline View (Alternative)

**Instead of spatial, show temporal:**

```
Timeline: 10:33 PM - 10:37 PM
────────────────────────────────────

10:33 │ Witness:  "The light is changing."
      │ Measurer: "2.3 degrees warmer."
      │ [silence]
      │
10:35 │ The One Who Knows: "Randomness is spiking."
      │ Parade: "The ceremony begins in five minutes."
      │ [Parade starts moving]
      │
10:37 │ Backward (while backing away): "I'm heading toward yesterday."
      │ The Listener: "That's not what you meant."
      │
```

**Shows:**
- Who said what when
- Pauses and silences
- Actions between dialogue
- Temporal flow

---

## 🔧 Implementation Plan

### Phase 2a: Fix Dialogue Output (DONE)
- ✅ Prompt now demands actual quotes
- ✅ NO "words are exchanged"
- ✅ YES "Character: 'actual words'"

### Phase 2b: Parse Dialogue
```python
def extract_dialogue(field_note_text):
    """
    Parse field notes for dialogue.
    Returns: [(speaker, quote), ...]
    """
    # Look for patterns:
    # - Character says, "quote"
    # - "Quote," Character says
    # - Character: "quote"
    pass
```

### Phase 2c: Visual Display Options

**Choose ONE to build first:**

**A) Speech Bubble Overlay** (Easiest)
- Add to field notes display
- Show dialogue in bubbles
- Color-coded by character
- ~1 day build

**B) Spatial Map** (Medium)
- Canvas/SVG top-down view
- Character positions
- Speech bubbles placed spatially
- ~3-5 days build

**C) Timeline View** (Medium)
- Vertical timeline
- Dialogue threaded
- Shows pauses
- ~2-3 days build

**D) Comic Panel Layout** (Advanced)
- Grid of panels
- Each panel = one exchange
- Speech bubbles
- Character illustrations
- ~1 week build

---

## 🎯 Your Suggestion: Map + Avatars

**I love this direction!** Here's how:

### Step 1: Basic Avatars (This Week)
- Create simple character icons
- Color-coded circles or symbols
- Shows who's speaking

### Step 2: Location Maps (Next Week)
- Simple top-down view of each location
- Place characters spatially
- Shows distances (Measurer approved!)

### Step 3: Speech Bubbles (Week 3)
- Overlay dialogue on map
- Click to expand/collapse
- Visual conversation flow

### Step 4: Animation (Month 2)
- Characters move on map
- Bubbles appear in sequence
- Spatial + temporal

---

## 📐 Technical Approach

### Data Structure:

```json
{
  "timestamp": "10:33 PM",
  "location": "courtyard",
  "characters": [
    {
      "id": "witness",
      "position": {"x": 0.3, "y": 0.5},
      "facing": "south",
      "dialogue": "The light is changing."
    },
    {
      "id": "measurer",
      "position": {"x": 0.3, "y": 0.7},
      "facing": "north",
      "dialogue": "2.3 degrees warmer."
    }
  ],
  "objects": [
    {"type": "rope", "position": {"x": 0.8, "y": 0.2}}
  ]
}
```

### Rendering:

**Canvas 2D:**
```javascript
// Draw location background
drawLocation(courtyard);

// Place characters
characters.forEach(char => {
  drawAvatar(char.id, char.position);
  if (char.dialogue) {
    drawSpeechBubble(char.dialogue, char.position);
  }
});

// Show distances (for Measurer!)
drawDistance(witness, measurer, "2.3m");
```

---

## 🎨 Immediate Fix

**For now (before visual map):**

The prompt now FORCES actual dialogue. Next simulation should show:

> Witness says, "The light is changing." Measurer stops. "2.3 degrees warmer," he responds.

Not:
> ~~Words are exchanged between Witness and Measurer.~~

---

## 🚀 Want Me To:

**A) Test current fix first** (restart server, should get real dialogue now)

**B) Build simple speech bubble view** (today - shows dialogue clearly)

**C) Build spatial map prototype** (this week - top-down with avatars)

**D) Both B + C** (full visual dialogue system)

---

**Let's test the prompt fix first, then I can build the visual map!**

Restart server and run again - dialogue should be ACTUAL QUOTES now! 🗣️
