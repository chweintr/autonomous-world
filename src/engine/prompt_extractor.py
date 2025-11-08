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
        
        # Composition description
        num_chars = len(interaction.characters_present)
        num_animals = len(interaction.animals_present)
        
        composition = f"{num_chars} figure{'s' if num_chars > 1 else ''}"
        if num_animals > 0:
            composition += f" + {num_animals} animal{'s' if num_animals > 1 else ''}"
        composition += f" at {interaction.location_name}. {interaction.time_of_day.title()} light."
        
        # Color notes (extract from material details)
        color_notes = interaction.material_details
        
        # Gesture notes (extract from action)
        gesture_notes = interaction.action_description.split('.')[0]  # First sentence
        
        # Painting prompt for artist
        painting_prompt = f"Paint this moment:\n\n"
        painting_prompt += f"{interaction.action_description}\n\n"
        painting_prompt += f"Focus on: {interaction.emotional_temperature.value} quality, "
        painting_prompt += f"the spatial arrangement, colors mentioned ({color_notes})"
        
        # Image generation prompt (for SD, Midjourney, etc.)
        image_gen_prompt = f"{interaction.action_description} "
        image_gen_prompt += f"{interaction.material_details} "
        image_gen_prompt += f"Cinematic, fashion editorial style, Thom Browne aesthetic, "
        image_gen_prompt += f"pink and aqua color palette, sculptural quality, "
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
            
            analysis_prompt = f"""Analyze this field note and extract painting/image generation prompts:

FIELD NOTE:
{interaction.to_field_note()}

Extract:
1. COMPOSITION: Describe the spatial arrangement (who where, how arranged, viewpoint)
2. COLOR: Key color relationships and palette
3. GESTURE: Most important gesture or physical detail
4. PAINTING_PROMPT: Directive for a painter (what to focus on, what makes it compelling)
5. IMAGE_GEN_PROMPT: Prompt for Stable Diffusion/Midjourney (technical, includes style keywords)
6. WHY_PAINTABLE: Why this moment is worth painting (1 sentence)

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
                    {"role": "system", "content": "You are an art director helping painters identify strong moments."},
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


