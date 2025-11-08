"""
Extracts paintable moments and generates prompts for artists and image generation.
"""
from typing import List, Dict, Tuple
from src.models.interaction import Interaction, EmotionalTemperature


class PaintablePrompt:
    """A prompt extracted from field notes for painting or image generation."""
    
    def __init__(
        self,
        source_interaction: Interaction,
        composition_description: str,
        color_notes: str,
        gesture_notes: str,
        painting_prompt: str,
        image_gen_prompt: str,
        why_paintable: str
    ):
        self.source_interaction = source_interaction
        self.composition_description = composition_description
        self.color_notes = color_notes
        self.gesture_notes = gesture_notes
        self.painting_prompt = painting_prompt
        self.image_gen_prompt = image_gen_prompt
        self.why_paintable = why_paintable
    
    def to_artist_prompt(self) -> str:
        """Format as prompt for the painter."""
        time_str = self.source_interaction.timestamp.strftime("%H:%M")
        
        prompt = f"=== PAINTABLE MOMENT [{time_str}] ===\n\n"
        prompt += f"LOCATION: {self.source_interaction.location_name}\n"
        prompt += f"EMOTIONAL CHARGE: {self.source_interaction.emotional_temperature.value}\n\n"
        
        prompt += f"COMPOSITION:\n{self.composition_description}\n\n"
        prompt += f"COLOR:\n{self.color_notes}\n\n"
        prompt += f"GESTURE/ACTION:\n{self.gesture_notes}\n\n"
        
        prompt += f"PAINTING PROMPT:\n{self.painting_prompt}\n\n"
        
        prompt += f"WHY THIS MOMENT:\n{self.why_paintable}\n"
        
        return prompt
    
    def to_image_gen_prompt(self) -> str:
        """Format as prompt for Stable Diffusion, Midjourney, etc."""
        return self.image_gen_prompt


class PromptExtractor:
    """Extracts paintable moments from simulation and generates prompts."""
    
    def __init__(self, use_llm: bool = False, api_key: str = None):
        """
        Args:
            use_llm: Use LLM to generate prompts (better quality)
            api_key: OpenAI API key for LLM mode
        """
        self.use_llm = use_llm
        self.api_key = api_key
    
    def extract_paintable_moments(
        self,
        interactions: List[Interaction],
        top_n: int = 5
    ) -> List[PaintablePrompt]:
        """
        Extract the most paintable moments from a session.
        
        Criteria for "paintable":
        - Strong emotional temperature (charged, tense, ruptured)
        - Rich color/material details
        - Clear spatial arrangement
        - Unexpected/emergent behavior
        - Dialogue with tension
        - Multiple characters/animals
        """
        scored_moments = []
        
        for interaction in interactions:
            score = self._score_paintability(interaction)
            scored_moments.append((score, interaction))
        
        # Sort by score, take top N
        scored_moments.sort(reverse=True, key=lambda x: x[0])
        top_moments = [interaction for score, interaction in scored_moments[:top_n]]
        
        # Generate prompts for top moments
        prompts = []
        for interaction in top_moments:
            prompt = self._generate_prompts(interaction)
            prompts.append(prompt)
        
        return prompts
    
    def _score_paintability(self, interaction: Interaction) -> float:
        """Score how paintable a moment is (0-10)."""
        score = 0.0
        
        # Emotional charge (max 3 points)
        charge_scores = {
            EmotionalTemperature.CHARGED: 3.0,
            EmotionalTemperature.TENSE: 2.5,
            EmotionalTemperature.RUPTURED: 3.0,
            EmotionalTemperature.RITUAL: 2.0,
            EmotionalTemperature.AGGRESSIVE: 2.0,
            EmotionalTemperature.TENDER: 1.5,
            EmotionalTemperature.EXUBERANT: 2.0,
            EmotionalTemperature.MELANCHOLIC: 1.5,
            EmotionalTemperature.UNCERTAIN: 1.0
        }
        score += charge_scores.get(interaction.emotional_temperature, 0)
        
        # Multiple characters (max 2 points)
        score += min(len(interaction.characters_present) * 0.5, 2.0)
        
        # Animals present (max 1 point)
        score += min(len(interaction.animals_present) * 0.3, 1.0)
        
        # Emergent behavior (bonus 2 points)
        if interaction.is_unexpected:
            score += 2.0
        
        # Rich material details (check for color words)
        color_words = ['pink', 'aqua', 'yellow', 'green', 'white', 'chrome', 'gold']
        material_lower = interaction.material_details.lower()
        colors_mentioned = sum(1 for color in color_words if color in material_lower)
        score += min(colors_mentioned * 0.5, 2.0)
        
        return score
    
    def _generate_prompts(self, interaction: Interaction) -> PaintablePrompt:
        """Generate painting and image-gen prompts for a moment."""
        
        if self.use_llm:
            return self._generate_prompts_llm(interaction)
        else:
            return self._generate_prompts_template(interaction)
    
    def _generate_prompts_template(self, interaction: Interaction) -> PaintablePrompt:
        """Generate prompts using templates (fast, no LLM)."""
        
        # Composition with structure: vantage, scene, light, weather
        import random
        vantages = ["Eye level", "Low angle looking up", "High angle looking down", "From behind", "Three-quarter view", "Profile view"]

        num_chars = len(interaction.characters_present)
        num_animals = len(interaction.animals_present)

        composition = f"Vantage: {random.choice(vantages)}. "
        composition += f"Scene: {num_chars} figure{'s' if num_chars > 1 else ''}"
        if num_animals > 0:
            composition += f" + {num_animals} animal{'s' if num_animals > 1 else ''}"
        composition += f" at {interaction.location_name}. "
        composition += f"Light: {interaction.time_of_day}. "
        composition += f"Atmosphere: {random.choice(['clear', 'hazy', 'dust-heavy', 'still air'])}."

        # Color notes (extract specific colors from material details)
        color_notes = interaction.material_details

        # Gesture notes (extract from action)
        gesture_notes = interaction.action_description.split('.')[0]  # First sentence

        # Conversational painting prompt for CALEB
        conversation_starters = [
            "CALEB, consider this:",
            "CALEB, what do you think about",
            "CALEB, this caught my eye:",
            "CALEB, look at"
        ]
        painting_prompt = f"{random.choice(conversation_starters)} {interaction.action_description}\n\n"
        painting_prompt += f"What interests me: the {interaction.emotional_temperature.value} quality between these figures. "
        painting_prompt += f"How would you handle {random.choice(['the spatial tension', 'the gesture', 'the light quality', 'the color relationships'])}?"

        # Image generation prompt - technical lighting/camera terms
        import random
        lighting_terms = ["low contrast", "high contrast", "diffuse light", "god rays", "heavy atmosphere", "low value", "splintering light", "direct overhead light", "raking sidelight"]
        vantage_terms = ["eye level", "low angle looking up", "high angle looking down", "from behind", "three-quarter view", "profile view"]
        texture_terms = ["fabric weight visible", "surface sheen", "matte finish", "crisp edges", "soft focus background"]

        image_gen_prompt = f"{interaction.action_description} "
        image_gen_prompt += f"{interaction.material_details} "
        image_gen_prompt += f"{random.choice(lighting_terms)}, {random.choice(vantage_terms)}, "
        image_gen_prompt += f"{random.choice(texture_terms)}, sculptural quality, "
        image_gen_prompt += f"{interaction.emotional_temperature.value} mood"
        
        # Why paintable
        why = f"Strong {interaction.emotional_temperature.value} charge"
        if interaction.is_unexpected:
            why += ", emergent behavior"
        if len(interaction.characters_present) > 1:
            why += f", {len(interaction.characters_present)} figures interacting"
        
        return PaintablePrompt(
            source_interaction=interaction,
            composition_description=composition,
            color_notes=color_notes,
            gesture_notes=gesture_notes,
            painting_prompt=painting_prompt,
            image_gen_prompt=image_gen_prompt,
            why_paintable=why
        )
    
    def _generate_prompts_llm(self, interaction: Interaction) -> PaintablePrompt:
        """Generate prompts using LLM (higher quality, costs $)."""
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            analysis_prompt = f"""Analyze this field note and extract painting/image generation prompts for CALEB (the painter):

FIELD NOTE:
{interaction.to_field_note()}

Extract these elements:

1. COMPOSITION - Structure this as:
   - Vantage: (eye level? low angle looking up? high angle? from behind? three-quarter?)
   - Scene arrangement: who is where, spatial relationship
   - Light quality: describe how light hits the scene
   - Weather/atmosphere: what's the air like?

2. COLOR: Key color relationships - be specific about where colors appear and how they relate

3. GESTURE: The key physical moment - what's the gesture/posture that defines this?

4. PAINTING_PROMPT: Write conversationally to CALEB. Like you're talking to a friend.
   - Start with: "CALEB, consider this:" or "CALEB, what do you think about..."
   - Describe what's compelling about THIS moment
   - Ask questions: "How would you handle...?" "What if you focused on...?"
   - Be conversational, not directive

5. IMAGE_GEN_PROMPT: Technical prompt for AI image generation
   - Vantage point (specific)
   - Lighting (technical terms, not generic)
   - Atmospheric quality
   - Key compositional elements
   - Texture/surface qualities

   🚨 VARY your language. Don't repeat same technical terms.

6. WHY_PAINTABLE: One sentence - what makes this worth capturing?

Format as JSON:
{{
  "composition": "...",
  "color": "...",
  "gesture": "...",
  "painting_prompt": "...",
  "image_gen_prompt": "...",
  "why_paintable": "..."
}}
"""
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an art director helping CALEB (the painter) identify strong moments. Use technical photography/lighting terms, not style references. Describe vantage point, contrast, light quality, texture."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            import json
            result = response.choices[0].message.content
            
            # Parse JSON
            if "{" in result:
                json_start = result.index("{")
                json_end = result.rindex("}") + 1
                data = json.loads(result[json_start:json_end])
                
                return PaintablePrompt(
                    source_interaction=interaction,
                    composition_description=data.get("composition", ""),
                    color_notes=data.get("color", ""),
                    gesture_notes=data.get("gesture", ""),
                    painting_prompt=data.get("painting_prompt", ""),
                    image_gen_prompt=data.get("image_gen_prompt", ""),
                    why_paintable=data.get("why_paintable", "")
                )
        
        except Exception as e:
            print(f"LLM prompt extraction failed: {e}. Using templates.")
            return self._generate_prompts_template(interaction)
        
        return self._generate_prompts_template(interaction)


