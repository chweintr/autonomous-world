"""
LLM-based description generator for vivid field notes.

This module can be configured to use different LLM backends:
- OpenAI API (GPT-4, GPT-3.5)
- Anthropic Claude
- Local models via Ollama
- Or fallback to template-based generation
"""
import os
import json
from typing import Optional, Dict, List
from datetime import datetime

from src.models.character import Character
from src.models.location import Location
from src.models.interaction import InteractionType, EmotionalTemperature


class DescriptionGenerator:
    """Generates vivid, specific descriptions for interactions."""
    
    def __init__(self, use_llm: bool = True, api_key: Optional[str] = None,
                 model: str = "gpt-4o"):
        """
        Args:
            use_llm: If True, use LLM. If False, use templates.
            api_key: API key for LLM service (or set OPENAI_API_KEY env var)
            model: Model name (gpt-4o, gpt-4, gpt-3.5-turbo, etc.)
        """
        self.use_llm = use_llm
        self.model = model
        
        if use_llm:
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                print("=" * 80)
                print("⚠️  ⚠️  ⚠️  WARNING: NO API KEY FOUND ⚠️  ⚠️  ⚠️")
                print("Set OPENAI_API_KEY in environment variables to use LLM mode.")
                print("Falling back to TEMPLATE-BASED GENERATION (limited variety)")
                print("=" * 80)
                self.use_llm = False
            else:
                print(f"✓ LLM mode enabled with model: {self.model}")
                print(f"✓ API key found: {self.api_key[:8]}...{self.api_key[-4:]}")
    
    def generate_interaction_description(
        self,
        interaction_type: InteractionType,
        location: Location,
        characters: List[Character],
        action_context: str,
        time_of_day: str,
        weather: str
    ) -> tuple[str, str, EmotionalTemperature]:
        """
        Generate vivid description of an interaction.
        
        Returns:
            (action_description, material_details, emotional_temperature)
        """
        if self.use_llm:
            return self._generate_with_llm(interaction_type, location, characters,
                                          action_context, time_of_day, weather)
        else:
            return self._generate_with_template(interaction_type, location, characters,
                                               action_context, time_of_day, weather)
    
    def _generate_with_llm(
        self,
        interaction_type: InteractionType,
        location: Location,
        characters: List[Character],
        action_context: str,
        time_of_day: str,
        weather: str
    ) -> tuple[str, str, EmotionalTemperature]:
        """Generate description using LLM."""
        
        # Build context for the LLM
        prompt = self._build_prompt(interaction_type, location, characters,
                                   action_context, time_of_day, weather)
        
        try:
            # Try to use OpenAI API (new v1.0+ syntax)
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            print(f"🤖 Calling LLM ({self.model}) for interaction description...")
            
            # Few-shot examples showing variety AND conversation
            import random

            few_shot_examples = [
                {
                    "role": "assistant",
                    "content": """{
  "action": "Measurer stops mid-step. \\"3.7 meters,\\" he announces. Collector looks up. \\"Between what?\\" The tape extends. \\"You and the nearest fallen thing.\\"",
  "material_details": "Dust rises where Measurer's boot disturbs ground. Sleeve - aqua thread spiraling through white linen - shifts as arm gestures with measuring tape.",
  "emotional_temperature": "playful"
}"""
                },
                {
                    "role": "assistant",
                    "content": """{
  "action": "\\"Still here?\\" Tuesday asks. The Listener doesn't answer. Or does, but not aloud. Tuesday adjusts the suitcase. The Listener nods at something unspoken.",
  "material_details": "Chrome handle catches overhead glare as suitcase shifts position. Jacket fabric - navy with pale stripe - folds differently as Tuesday's weight changes.",
  "emotional_temperature": "tense"
}"""
                },
                {
                    "role": "assistant",
                    "content": """{
  "action": "Backward: \\"Tomorrow I saw you here.\\" Parade tilts head. \\"Was I performing?\\" Backward considers the future-past. \\"You will have been.\\"",
  "material_details": "Afternoon light fractures through suspended dust. Embroidery - green branching pattern - becomes visible as fabric stretches with Parade's movement.",
  "emotional_temperature": "ritual"
}"""
                }
            ]

            # Pick 1-2 examples randomly to show variety
            few_shot_example = random.choice(few_shot_examples)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": "Generate a field note with Measurer and Collector talking."},
                    few_shot_example,  # Show example with actual dialogue
                    {"role": "user", "content": prompt}
                ],
                temperature=1.8,  # EXTREME creativity - force maximum variety
                max_tokens=350,
                presence_penalty=1.0,  # Maximum penalty for repetition
                frequency_penalty=1.0   # Maximum penalty for repeated words
            )
            
            result = response.choices[0].message.content
            return self._parse_llm_response(result)
            
        except Exception as e:
            print(f"LLM generation failed: {e}. Falling back to templates.")
            return self._generate_with_template(interaction_type, location, characters,
                                               action_context, time_of_day, weather)
    
    def _build_prompt(
        self,
        interaction_type: InteractionType,
        location: Location,
        characters: List[Character],
        action_context: str,
        time_of_day: str,
        weather: str
    ) -> str:
        """Build prompt for LLM."""
        
        char_descriptions = []
        for char in characters:
            desc = f"- {char.name} ({char.archetype}): Currently {char.emotional_state.value}"
            
            # Add recent memories for context
            recent_memories = char.get_recent_memories(count=3)
            if recent_memories:
                memory_context = " | Recent memories: "
                memory_context += "; ".join([m.content[:30] + "..." for m in recent_memories])
                desc += memory_context
            
            char_descriptions.append(desc)
        
        # Check for shared history between characters
        history_note = ""
        if len(characters) == 2:
            char1, char2 = characters
            past_meetings = char1.get_memories_about(char2.id, limit=3)
            if past_meetings:
                history_note = f"\n\n🔁 CONVERSATION HISTORY (what they said to each other recently):"
                for mem in past_meetings[-3:]:  # Last 3 interactions
                    history_note += f"\n- {mem.content[:100]}"
                history_note += "\n\n⚠️ CRITICAL: They are CONTINUING this conversation. DON'T repeat what was already said. Have them RESPOND and move the conversation forward."
        
        prompt = f"""Generate a field note for this moment:

LOCATION: {location.name}
TIME: {time_of_day}, {weather}

CHARACTERS PRESENT:
{chr(10).join(char_descriptions)}{history_note}

ACTION CONTEXT: {action_context}

CHARACTER VOICES (let them speak naturally in their style):
- Measurer: Quantifies abstract things, announces measurements
- The One Who Knows: References meta/simulation concepts as if they're weather
- Collector: Asks about lost things, returns dropped words from earlier
- The Listener: Responds to what wasn't said, mishears deliberately
- Backward: Confuses past and future direction in speech
- Parade: Announces ceremonies, assigns roles to no-one
- Forget-Nothing: Corrects minor details, cites old conversations
- Bird Gatherer: Minimal speech, deflects questions about birds
- Tuesday: Evasive about the suitcase, smiles
- Sleeper: Delayed responses, dream-logic answers

Generate like a SCREENPLAY with SPOKEN DIALOGUE:

1. ACTION (2-3 sentences): 

IF 2+ CHARACTERS: Write dialogue like this:
Measurer: "3.7 meters between us."
Tuesday: "Between what?"
Measurer: "You and the truth."

OR like this:
"Have you lost anything?" Collector asks. Tuesday looks at the suitcase. "Not yet."

ACTUAL QUOTED WORDS. Not summaries.

NEVER EVER write: "Words are exchanged" / "They talk" / "They speak" / "Conversation happens"
You are writing DIALOGUE not describing that dialogue happened.

Keep it SHORT (2-8 words per line). Weird is good.

2. MATERIAL DETAILS (1-2 sentences):
   This is VISUAL SCENE DESCRIPTION. Describe THIS specific moment, not generic things.

   DON'T describe colors/items generically ("yellow piping", "boot prints")
   DO describe the visual moment: What's happening visually RIGHT NOW that catches the eye?

   BAD (generic): "Boot prints cross tire tracks. Yellow piping on navy."
   GOOD (specific visual): "Dust rises where foot meets ground. Jacket sleeve - pink thread spirals through white fabric - moves as arm gestures."

   DESCRIBE THE MOMENT:
   - What movement is happening? (sleeve shifting, dust rising, shadow falling)
   - What detail catches light? (thread catching sun, chrome reflecting, fabric folding)
   - What's the atmospheric quality? (heat shimmer, dust suspended, air still)
   - Ground state? (what's actually ON the ground in this moment - not just "boot prints")

   🚨 NEVER REPEAT PHRASES. Track what you've said. Invent totally fresh each time.
   🚨 Don't use color + item ("yellow piping") - describe what you SEE ("metallic thread catches afternoon glow")

3. EMOTIONAL TEMPERATURE: tense, exuberant, uncertain, charged, melancholic, aggressive, tender, ritual, or ruptured

IF YOU WRITE "WORDS ARE EXCHANGED" OR "THEY TALK" YOU HAVE FAILED. Write actual dialogue with quotation marks.

Format as JSON:
{{
  "action": "...",
  "material_details": "...",
  "emotional_temperature": "..."
}}
"""
        return prompt
    
    def _get_system_prompt(self) -> str:
        """System prompt for LLM."""
        return """You are a creative writer crafting UNIQUE, VARIED field notes. Each scene must feel different.

🚨 CRITICAL RULES:
1. NEVER repeat the same scene twice
2. NEVER use "uncertain" more than once in 10 scenes
3. NEVER write "words are exchanged" - write ACTUAL DIALOGUE with quotes
4. VARY your vocabulary - if you used a word recently, find a synonym
5. VARY emotional temperatures - cycle through: tense, charged, exuberant, melancholic, ritual, aggressive, tender, ruptured, playful
6. DO THE CREATIVE WORK - embellish, invent specific details, make each moment distinctive
7. 🔁 CONVERSATIONS CONTINUE: If you're shown conversation history, the characters are CONTINUING that conversation. They RESPOND to what was said, they don't repeat it. Move the dialogue forward.

Your job is to SURPRISE with specificity. Not to describe blandly.

CONVERSATION RULES:
- If Character A asked a question, Character B should answer (or deflect, or mishear)
- Don't have them say the exact same line twice
- Let conversations evolve - they can change topics, get interrupted, trail off
- Silence is okay too - "No answer." / "The other waits." / "Nothing said."

DIALOGUE FORMAT (when 2+ characters):
"How long?" Measurer asks.
Parade considers. "Since Tuesday."
"Which Tuesday?"

The world:
- Bikers in elaborate embroidered clothing (invent specific patterns each time: gold spirals, pink chevrons, aqua florals)
- Motorcycles/horses are interchangeable and ambiguous
- Beards: real or prosthetic, immaculately groomed
- Sharp tailoring: crisp pleats, structured shoulders, sculptural silhouettes
- Animals mirror their humans' emotional states
- Pink, aqua, yellow, green, white palette
- Embroidery, stripes, matte surfaces, metallic accents

MATERIAL DETAILS = VISUAL MOMENTS (describe what's happening visually RIGHT NOW):

DON'T write generic lists: "Boot prints. Yellow piping. Chrome."
DO describe the visual moment: "Dust rises where boot meets ground. Thread - metallic, catching sun - visible as sleeve moves."

EXAMPLES (for inspiration - NEVER COPY):
- "Air shimmers with heat. Embroidery pattern - pink spirals - emerges as fabric stretches."
- "Shadow falls across scene as figure shifts. Chrome reflects distorted shapes."
- "Light fractures through suspended particles. Jacket hem reveals lining contrast as body turns."
- "Ground where boot disturbed shows darker earth beneath. Thread catches afternoon glow."

DESCRIBE MOVEMENT + LIGHT + SPECIFIC DETAIL:
✓ What's moving? (sleeve, shadow, dust)
✓ How's light hitting? (catching, fracturing, reflecting)
✓ What specific detail emerges? (embroidery visible, color contrast, surface texture)

🚨 IF YOU WRITE SAME PHRASE TWICE ("boot prints cross") YOU FAIL
🚨 IF YOU USE GENERIC COLOR+ITEM ("yellow piping") YOU FAIL
🚨 DESCRIBE THE VISUAL MOMENT, NOT INVENTORY OF THINGS

BE CREATIVE. BE SPECIFIC. BE VARIED. Don't phone it in."""
    
    def _parse_llm_response(self, response: str) -> tuple[str, str, EmotionalTemperature]:
        """Parse LLM JSON response."""
        try:
            # Try to parse as JSON
            if "{" in response:
                json_start = response.index("{")
                json_end = response.rindex("}") + 1
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                
                action = data.get("action", "")
                material = data.get("material_details", "")
                temp_str = data.get("emotional_temperature", "uncertain").lower()
                
                # Map to EmotionalTemperature enum
                temp_mapping = {
                    "tense": EmotionalTemperature.TENSE,
                    "exuberant": EmotionalTemperature.EXUBERANT,
                    "uncertain": EmotionalTemperature.UNCERTAIN,
                    "charged": EmotionalTemperature.CHARGED,
                    "melancholic": EmotionalTemperature.MELANCHOLIC,
                    "playful": EmotionalTemperature.PLAYFUL,
                    "aggressive": EmotionalTemperature.AGGRESSIVE,
                    "tender": EmotionalTemperature.TENDER,
                    "ritual": EmotionalTemperature.RITUAL,
                    "ruptured": EmotionalTemperature.RUPTURED
                }
                
                temp = temp_mapping.get(temp_str, EmotionalTemperature.UNCERTAIN)
                
                return action, material, temp
        except:
            pass
        
        # Fallback parsing
        lines = response.strip().split("\n")
        action = lines[0] if lines else ""
        material = lines[1] if len(lines) > 1 else ""
        return action, material, EmotionalTemperature.UNCERTAIN
    
    def _generate_with_template(
        self,
        interaction_type: InteractionType,
        location: Location,
        characters: List[Character],
        action_context: str,
        time_of_day: str,
        weather: str
    ) -> tuple[str, str, EmotionalTemperature]:
        """Generate description using templates (fallback when no LLM)."""
        
        import random
        
        # Build action description from templates
        char_names = [c.name for c in characters]
        animals = [c.animal_companion.name for c in characters]
        
        if interaction_type == InteractionType.CHARACTER_TO_CHARACTER:
            # Generate varied dialogue - random each time
            questions = [
                "How many days?", "Where's the horse?", "Did you find it?",
                "What time is it?", "Who was here?", "What's that sound?",
                "Are we done?", "Is this the place?", "What did they say?",
                "When do we leave?", "Which one?", "Who told you?",
                "How far?", "What's missing?", "Why stop here?",
                "Is it Tuesday?", "What's broken?", "Who's counting?"
            ]

            responses = [
                "considers", "looks away", "doesn't answer", "shrugs",
                "waits", "glances at {animal}", "adjusts position",
                "looks at the horizon", "remains silent"
            ]

            response = random.choice(responses).format(animal=animals[0] if animals else "the animal")
            other_char = char_names[1] if len(char_names) > 1 else "the other"

            actions = [
                f'"{random.choice(questions)}" {char_names[0]} asks. {other_char} {response}.',
                f'{char_names[0]} and {other_char} face each other. "{random.choice(questions)}" {animals[0] if animals else "The animal"} watches.',
                f'"{random.choice(questions)}" {other_char}: "Tomorrow." {char_names[0]} nods.'
            ]
        elif interaction_type == InteractionType.CHARACTER_TO_ANIMAL:
            actions = [
                f"{char_names[0]} reaches toward {animals[0]}. The animal's response is uncertain. A moment of contact, then separation.",
                f"{animals[0]} circles {char_names[0]}. The human stands still, waiting. Connection hovers, unresolved.",
                f"{char_names[0]}'s hands move over {animals[0]}'s form. The gesture could be care or control. The animal endures."
            ]
        elif interaction_type == InteractionType.OBSERVATION:
            actions = [
                f"{char_names[0]} stands motionless in the space. {animals[0]} nearby, equally still. Time seems suspended.",
                f"Nothing happens. {char_names[0]} and {animals[0]} occupy the space without action. Presence itself becomes the event.",
                f"{char_names[0]} watches the horizon. {animals[0]} grazes or rests. The quality of waiting intensifies."
            ]
        else:
            actions = [
                f"{char_names[0]} interacts with {location.objects_present[0] if location.objects_present else 'the environment'}. {action_context}",
                f"Movement in the space. {char_names[0]} and {animals[0]} navigate the terrain. {action_context}"
            ]
        
        action = random.choice(actions)
        
        # Material details - generate random combinations
        movements = [
            "Dust lifts", "Fabric shifts", "Shadow moves", "Boot scuffs ground",
            "Hand gestures", "Body turns", "Weight shifts", "Posture changes",
            "Arm extends", "Head tilts", "Leg extends", "Shoulder drops"
        ]

        where = [
            "as figure moves", "with the gesture", "during the pause",
            "in the moment", "as words spoken", "while waiting",
            "at the exchange", "during stillness", "in the silence"
        ]

        visual_elements = [
            f"Embroidery - {random.choice(['pink', 'aqua', 'yellow', 'green'])} {random.choice(['spirals', 'chevrons', 'florals', 'stripes'])} - catches light",
            f"Thread - metallic - {random.choice(['visible', 'gleaming', 'catching glow', 'reflects'])}",
            f"{random.choice(['Chrome', 'Metal', 'Polished surface'])} {random.choice(['reflects', 'mirrors', 'catches', 'distorts'])} {random.choice(['scene', 'surroundings', 'light', 'shapes'])}",
            f"Lining - {random.choice(['contrasting', 'pale', 'dark', 'bright'])} {random.choice(['pink', 'aqua', 'white', 'yellow'])} - {random.choice(['visible', 'revealed', 'shows', 'emerges'])}",
            f"Ground shows {random.choice(['boot marks', 'disturbed earth', 'compressed surface', 'scuff marks', 'fresh impressions'])}"
        ]

        atmosphere = [
            f"{time_of_day.capitalize()} {random.choice(['light', 'glow', 'sun'])} {random.choice(['diffuses', 'fractures', 'scatters', 'illuminates'])}",
            f"Air {random.choice(['thick', 'heavy', 'still', 'shimmering'])} with {random.choice(['heat', 'dust', 'particles', 'haze'])}",
            f"{weather.capitalize()} sky {random.choice(['overhead', 'above', 'stretching', 'looming'])}"
        ]

        # Randomly combine elements
        material = f"{random.choice(movements)} {random.choice(where)}. {random.choice(visual_elements)}. {random.choice(atmosphere)}."
        
        # Emotional temperature based on characters' states
        avg_intensity = sum(c.emotional_intensity for c in characters) / len(characters)
        
        if avg_intensity > 0.7:
            temp = random.choice([EmotionalTemperature.TENSE, EmotionalTemperature.CHARGED, 
                                EmotionalTemperature.AGGRESSIVE])
        elif avg_intensity < 0.3:
            temp = random.choice([EmotionalTemperature.UNCERTAIN, EmotionalTemperature.MELANCHOLIC])
        else:
            temp = random.choice([EmotionalTemperature.UNCERTAIN, EmotionalTemperature.TENDER,
                                EmotionalTemperature.PLAYFUL])
        
        return action, material, temp

