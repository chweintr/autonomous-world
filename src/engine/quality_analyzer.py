"""
Quality analyzer that detects repetition and provides feedback.
"""
from typing import List, Dict, Tuple
from collections import Counter
import re
from src.models.interaction import Interaction


class QualityAnalyzer:
    """Analyzes interactions for repetition and quality issues."""

    def __init__(self):
        # Words to avoid repeating
        self.watch_words = [
            'functional', 'uncertain', 'uneasy', 'tension', 'charged',
            'watches', 'stands', 'motionless', 'suspended', 'holds'
        ]

        # Track scene patterns
        self.scene_signatures = []

    def analyze_session(self, interactions: List[Interaction]) -> Dict:
        """
        Analyze a full session for quality issues.

        Returns dict with:
        - word_frequency: Most common words
        - overused_words: Words appearing too frequently
        - repetitive_scenes: Similar scenes
        - suggestions: List of improvement suggestions
        """
        all_text = ' '.join([
            f"{i.action_description} {i.material_details}"
            for i in interactions
        ])

        # Word frequency analysis
        words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())
        word_freq = Counter(words)

        # Find overused words
        overused = {}
        total_interactions = len(interactions)
        for word in self.watch_words:
            count = word_freq.get(word, 0)
            if count > total_interactions * 0.3:  # More than 30% of scenes
                overused[word] = count

        # Detect scene repetition
        scene_patterns = self._detect_scene_patterns(interactions)

        # Generate suggestions
        suggestions = []

        if overused:
            suggestions.append({
                'type': 'overused_words',
                'severity': 'high',
                'message': f"Overused words detected: {', '.join(overused.keys())}",
                'detail': f"These words appear in >30% of interactions. Vary vocabulary.",
                'examples': overused
            })

        if scene_patterns['repetitive_locations']:
            suggestions.append({
                'type': 'repetitive_locations',
                'severity': 'medium',
                'message': f"Same locations repeated: {', '.join(scene_patterns['repetitive_locations'][:3])}",
                'detail': "Consider moving characters to varied locations."
            })

        if scene_patterns['repetitive_pairings']:
            suggestions.append({
                'type': 'repetitive_pairings',
                'severity': 'medium',
                'message': f"Same character pairings repeated",
                'detail': f"These pairs interact frequently: {', '.join(scene_patterns['repetitive_pairings'][:3])}",
                'action': "Introduce new character combinations."
            })

        # Check emotional temperature variety
        temps = [i.emotional_temperature.value for i in interactions]
        temp_freq = Counter(temps)
        if len(temp_freq) < 4:  # Only using 3 or fewer temperature types
            suggestions.append({
                'type': 'limited_emotional_range',
                'severity': 'medium',
                'message': f"Limited emotional variety",
                'detail': f"Using mostly: {', '.join([k for k,v in temp_freq.most_common(3)])}",
                'action': "Expand emotional temperature range in descriptions."
            })

        return {
            'word_frequency': dict(word_freq.most_common(20)),
            'overused_words': overused,
            'scene_patterns': scene_patterns,
            'suggestions': suggestions,
            'total_interactions': total_interactions
        }

    def _detect_scene_patterns(self, interactions: List[Interaction]) -> Dict:
        """Detect repeated scene patterns."""

        # Track location frequency
        locations = [i.location_name for i in interactions]
        location_freq = Counter(locations)
        repetitive_locations = [
            loc for loc, count in location_freq.items()
            if count > len(interactions) * 0.4  # Same location >40% of time
        ]

        # Track character pairings
        pairings = []
        for interaction in interactions:
            if len(interaction.characters_present) >= 2:
                pair = tuple(sorted(interaction.characters_present[:2]))
                pairings.append(pair)

        pairing_freq = Counter(pairings)
        repetitive_pairings = [
            f"{pair[0]} & {pair[1]}"
            for pair, count in pairing_freq.items()
            if count > len(pairings) * 0.5  # Same pair >50% of multi-character scenes
        ]

        return {
            'repetitive_locations': repetitive_locations,
            'location_distribution': dict(location_freq),
            'repetitive_pairings': repetitive_pairings,
            'total_unique_pairings': len(pairing_freq)
        }

    def get_alternative_words(self, overused_word: str) -> List[str]:
        """Suggest alternatives for overused words."""

        alternatives = {
            'functional': ['utilitarian', 'practical', 'plain', 'unadorned', 'simple', 'stark', 'minimal'],
            'uncertain': ['ambiguous', 'unclear', 'indeterminate', 'wavering', 'hesitant', 'questioning'],
            'uneasy': ['tense', 'unsettled', 'agitated', 'restless', 'anxious', 'wary'],
            'tension': ['strain', 'pressure', 'stress', 'charge', 'friction'],
            'charged': ['electric', 'intense', 'loaded', 'fraught', 'volatile'],
            'watches': ['observes', 'regards', 'studies', 'monitors', 'tracks', 'follows'],
            'stands': ['remains', 'holds position', 'stays', 'waits', 'lingers'],
            'motionless': ['still', 'frozen', 'stationary', 'static', 'immobile', 'fixed'],
            'suspended': ['held', 'hanging', 'paused', 'arrested', 'halted'],
            'holds': ['maintains', 'keeps', 'sustains', 'preserves', 'retains']
        }

        return alternatives.get(overused_word.lower(), [])
