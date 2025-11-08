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
                 model: str = "gpt-4"):
        """
        Args:
            use_llm: If True, use LLM. If False, use templates.
            api_key: API key for LLM service (or set OPENAI_API_KEY env var)
            model: Model name (gpt-4, gpt-3.5-turbo, claude-3, etc.)
        """
        self.use_llm = use_llm
        self.model = model
        
        if use_llm:
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            if not self.api_key:
                print("Warning: No API key provided. Falling back to template-based generation.")
                self.use_llm = False
    
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
            
            # Few-shot example to show correct dialogue format
            few_shot_example = {
                "role": "assistant",
                "content": """{
  "action": "Measurer stops mid-step. \\"3.7 meters,\\" he announces. Collector looks up from the ground. \\"Between what?\\" Measurer extends the tape. \\"You and the nearest fallen thing.\\"",
  "material_details": "Aqua blazer against pink ground. Measuring tape bright yellow.",
  "emotional_temperature": "playful"
}"""
            }
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": "Generate a field note with Measurer and Collector talking."},
                    few_shot_example,  # Show example with actual dialogue
                    {"role": "user", "content": prompt}
                ],
                temperature=1.4,  # MAXIMUM creativity - force variety
                max_tokens=350,
                presence_penalty=0.6,  # Penalize repetition heavily
                frequency_penalty=0.8   # Strong penalty for repeated words
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
            past_meetings = char1.get_memories_about(char2.id, limit=2)
            if past_meetings:
                history_note = f"\nPAST INTERACTIONS: These characters have met before. "
                history_note += f"Last time: {past_meetings[-1].content[:60]}..."
        
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

2. MATERIAL DETAILS (1 sentence):
   - Lighting quality (diffuse/harsh/low contrast/raking/splintered/god rays)
   - Colors (pink/aqua/yellow/green/white preferred)
   - One material detail (embroidery pattern, stripe width, fabric weight, surface texture)
   - VARY your vocabulary - don't repeat "functional" or same descriptors
   - Examples: "Raking light across pink pinstripes. Navy wool, crisp." / "Diffuse glow. Aqua embroidery on white linen." / "Low contrast. Yellow stitching catches eye."

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

Your job is to SURPRISE with specificity. Not to describe blandly.

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

VARY YOUR MATERIAL DETAILS:
Don't repeat. Invent new combinations each time:
- "Pink herringbone. Wool weight."
- "Aqua chain-stitch on white linen. Crisp."
- "Yellow piping catches raking light. Matte navy."
- "Green embroidered spirals. Metallic thread."

VARY YOUR LIGHTING:
- God rays at low angle
- Diffuse overcast glow
- Raking sidelight, harsh shadows
- Direct overhead, high contrast
- Splintered through clouds
- Heavy atmosphere, low value

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
            # Generate simple dialogue instead of "words are exchanged"
            actions = [
                f'{char_names[0]}: "You again." {char_names[1] if len(char_names) > 1 else "The other"} nods. {animals[0]} watches.',
                f'{char_names[0]} and {char_names[1] if len(char_names) > 1 else "another figure"} stand facing each other. Silence. Then {char_names[0]}: "Still here?"',
                f'"{random.choice(["Lost anything?", "How long?", "Which direction?", "Same as yesterday?"])}" {char_names[0]} asks. {char_names[1] if len(char_names) > 1 else "The other"} considers. {animals[0]} shifts position.'
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
        
        # Material details - vary vocabulary, avoid "functional"
        lighting_variations = [
            f"Diffuse {time_of_day} light. {random.choice(['Low contrast', 'High contrast', 'Muted tones', 'Crisp shadows'])}.",
            f"{random.choice(['Raking sidelight', 'Direct overhead', 'Splintered through clouds', 'God rays at low angle'])}. Dust visible.",
            f"{random.choice(['Heavy atmosphere', 'Clear sharp air', 'Hazy distance', 'Crystalline quality'])}. {weather} colors the scene."
        ]

        material_variations = [
            f"Pink pinstripes on navy. {random.choice(['Wool weight', 'Linen crisp', 'Cotton soft', 'Stiff canvas'])}.",
            f"Aqua embroidery catches light. {random.choice(['Metallic thread', 'Matte stitching', 'Raised texture', 'Flat panels'])}.",
            f"{random.choice(['Yellow accents', 'Green piping', 'White trim', 'Pale edging'])} on structured jacket."
        ]

        materials = lighting_variations + material_variations
        
        material = random.choice(materials)
        
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

