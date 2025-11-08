# Character Memory System Design

## 🧠 Inspired by Stanford's Smallville Generative Agents

### The Problem (Current)

Characters have no memory! Each interaction is isolated:
- Measurer measures Collector's pockets
- 5 minutes later, does it again
- No continuity, no relationship development
- Dialogue can't reference past events

### The Solution: Memory Stream

Each character maintains a memory stream of:
- What they observed
- Who they interacted with
- What was said
- Important events
- Emotional impact

---

## 📊 Memory Structure

### Simple Version (Phase 2a):

```python
@dataclass
class Memory:
    timestamp: datetime
    type: str  # "observation", "interaction", "dialogue", "event"
    content: str  # What happened
    location: str
    other_characters: List[str]
    importance: float  # 0-10
    emotional_impact: float  # -1 to 1
```

### Character Memory Storage:

```python
@dataclass
class Character:
    ...
    memory_stream: List[Memory] = field(default_factory=list)
    
    def add_memory(self, memory: Memory):
        self.memory_stream.append(memory)
        # Keep only last 100 memories (or important ones)
        if len(self.memory_stream) > 100:
            self._prune_memories()
    
    def get_recent_memories(self, count: int = 5) -> List[Memory]:
        """Get recent memories for context."""
        return self.memory_stream[-count:]
    
    def get_memories_about(self, character_id: str) -> List[Memory]:
        """Get all memories involving another character."""
        return [m for m in self.memory_stream 
                if character_id in m.other_characters]
    
    def get_important_memories(self, threshold: float = 7.0) -> List[Memory]:
        """Get high-importance memories."""
        return [m for m in self.memory_stream 
                if m.importance >= threshold]
```

---

## 🎯 How It Makes Dialogue Natural

### Before (No Memory):
```
10:30 - Measurer meets Collector
Measurer: "May I measure your pockets?"
Collector: "Sure."

10:35 - Measurer meets Collector AGAIN
Measurer: "May I measure your pockets?"  # REPEATS!
Collector: "Sure."  # NO MEMORY!
```

### After (With Memory):
```
10:30 - Measurer meets Collector
Measurer: "May I measure your pockets?"
Collector: "Sure."
[Both store memory: "pocket measurement interaction"]

10:35 - Measurer meets Collector AGAIN
Decision engine checks: "Have we interacted before?"
Finds memory: "Yes, measured pockets 5 minutes ago"
Provides context: "Previous interaction: measured pockets"

LLM generates:
Collector: "You already measured them."
Measurer: "Measurements drift. 0.2cm difference."
```

**Natural continuity!**

---

## 🔄 Implementation Steps

### Step 1: Add Memory to Data Model

```python
# src/models/character.py

@dataclass
class Memory:
    timestamp: datetime
    content: str
    location: str
    other_characters: List[str]
    importance: float
    emotional_impact: float

@dataclass  
class Character:
    ...
    memory_stream: List[Memory] = field(default_factory=list)
```

### Step 2: Store Memories After Interactions

```python
# src/engine/simulation.py

def _execute_decision(...):
    ...
    # Create interaction
    interaction = Interaction(...)
    
    # Store memory in each character present
    for char in chars_present:
        memory = Memory(
            timestamp=interaction.timestamp,
            content=interaction.action_description,
            location=interaction.location_id,
            other_characters=[c.id for c in chars_present if c.id != char.id],
            importance=calculate_importance(interaction),
            emotional_impact=char.emotional_intensity
        )
        char.add_memory(memory)
```

### Step 3: Use Memory in Decisions

```python
# src/engine/decision_engine.py

def decide_action(character, location, others, ...):
    # Check if we've recently interacted with these characters
    for other in others:
        recent_memories = character.get_memories_about(other.id)
        
        if recent_memories:
            last_interaction = recent_memories[-1]
            context = f"Last met {other.name}: {last_interaction.content[:50]}"
            # Use this context in decision!
```

### Step 4: Provide Memory Context to LLM

```python
# When generating description, include recent memories:

RECENT MEMORIES (for dialogue context):
- 5 min ago: Measured Collector's pockets (42cm depth)
- 10 min ago: Collector asked if I'd lost anything

This informs what they might talk about NOW.
```

**LLM then generates:**
> Collector: "Still measuring?"  
> Measurer: "Always. Your pockets grew 0.3cm."

---

## 🗺️ Map Visualization (Smallville-Style)

### Simple Implementation:

**HTML/CSS Grid Map:**

```html
<div class="world-map">
  <!-- Grid layout of locations -->
  <div class="map-location courtyard" data-loc="courtyard">
    <h4>The Courtyard</h4>
    <div class="avatars">
      <div class="avatar" data-char="measurer">
        <span class="icon">📏</span>
        <span class="name">Measurer</span>
      </div>
      <div class="avatar" data-char="collector">
        <span class="icon">🎒</span>
        <span class="name">Collector</span>
      </div>
    </div>
  </div>
  
  <div class="map-location stable" data-loc="stable">
    <h4>Stable Ruin</h4>
    <div class="avatars">
      <div class="avatar" data-char="bird_gatherer">
        <span class="icon">🕊️</span>
        <span class="name">Bird Gatherer</span>
      </div>
    </div>
  </div>
  
  <!-- More locations... -->
</div>
```

**Updates via JavaScript:**
```javascript
// After each interaction, update map
function updateMap(characterId, newLocation) {
  const avatar = $(`.avatar[data-char="${characterId}"]`);
  const newLoc = $(`.map-location[data-loc="${newLocation}"]`);
  newLoc.querySelector('.avatars').appendChild(avatar);
}
```

**Click avatar:**
```javascript
on(avatar, 'click', () => {
  showCharacterMemories(characterId);
  showRecentDialogue(characterId);
});
```

---

## 📐 Layout Options

### Option A: Grid Map (Easiest)
```
┌─────────────┬─────────────┬─────────────┐
│ Courtyard   │ Stable Ruin │ Patterned   │
│ 👤M 👤C     │ 👤BG        │ Room        │
│             │             │ 👤W 👤P     │
├─────────────┼─────────────┼─────────────┤
│ Bonfire     │ Desert      │ Rooftop     │
│ 👤T         │ 👤B         │ 👤L         │
│             │             │             │
└─────────────┴─────────────┴─────────────┘
```

### Option B: Canvas/SVG (Better Looking)
- Draw actual spatial layout
- Avatars positioned precisely
- Lines showing movement
- Speech bubbles

### Option C: Phaser.js (Like Smallville)
- Actual game engine
- Smooth animations
- Click to interact
- Most work but most polished

---

## 🎯 My Recommendation

### **This Week: Add Memory System**
1. Add Memory data model
2. Store memories after interactions
3. Retrieve memories for context
4. Dialogue becomes continuous

**Result:** "You asked me that yesterday" / "We already measured this" / etc.

### **Next Week: Simple Map View**
1. Grid layout of locations
2. Emoji/icon avatars
3. Updates after interactions
4. Click to see memories

**Result:** Visual sense of where everyone is

### **Month 2: Animated Map**
1. Canvas or Phaser.js
2. Characters move
3. Speech bubbles
4. Like Smallville

---

## 💾 Quick Implementation Estimate

### **Memory System:**
- **Time:** 2-3 hours
- **Complexity:** Low-medium
- **Impact:** HUGE (enables natural dialogue)

### **Simple Grid Map:**
- **Time:** 3-4 hours
- **Complexity:** Low
- **Impact:** Good spatial awareness

### **Canvas/Animated Map:**
- **Time:** 1-2 days
- **Complexity:** Medium
- **Impact:** Beautiful, like Smallville

---

## 🚀 **Want Me To:**

**A)** Build memory system first (enables natural dialogue based on history)

**B)** Build simple map first (visual spatial awareness)

**C)** Both in parallel (memory for backend, map for frontend)

**My vote: A first** - memory makes dialogue actually work, then we can visualize it!

Should I start building the memory system? 🧠
