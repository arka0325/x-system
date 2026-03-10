class KnowledgeIntelligenceLayer:

    def __init__(self):
        self.framework = self._load_framework()

    def _load_framework(self):

        return {

            "Awareness_with_Emotion": {
                "measurement_variable": "Emotional Memory Strength",
                "high_definition": [
                    "Clear emotional trigger",
                    "Repetition of emotional theme",
                    "Strong narrative contrast",
                    "Memorable positioning language"
                ],
                "weak_pattern": [
                    "Generic tone",
                    "Inconsistent storytelling",
                    "No emotional anchor"
                ]
            },

            "Positioning_with_Insight": {
                "measurement_variable": "Territory Insight Strength",
                "high_definition": [
                    "Clear category framing",
                    "Strong differentiation",
                    "Defined target niche",
                    "Original strategic insight"
                ],
                "weak_pattern": [
                    "Generic market language",
                    "No competitive contrast",
                    "Broad audience messaging"
                ]
            },

            "Logic_with_Trust": {
                "measurement_variable": "Trust Coherence Strength",
                "high_definition": [
                    "Visible case studies",
                    "Specific claims",
                    "Proof-backed messaging",
                    "Authority markers"
                ],
                "weak_pattern": [
                    "Claims without proof",
                    "Vague testimonials",
                    "No evidence structure"
                ]
            },

            "Lead_with_Value": {
                "measurement_variable": "Value Perception Strength",
                "high_definition": [
                    "Clear outcome visibility",
                    "Strong CTA alignment",
                    "Mechanism explained",
                    "Benefit clarity"
                ],
                "weak_pattern": [
                    "Unclear offer",
                    "Feature-heavy messaging",
                    "Weak CTA"
                ]
            }
        }

    def get_framework(self):
        return self.framework