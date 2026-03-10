class PillarPermutationEngine:

    def evaluate(self, scoring_json):
        pillar_scores = {
            "Awareness_with_Emotion": self._extract_score(scoring_json, "Awareness_with_Emotion"),
            "Positioning_with_Insight": self._extract_score(scoring_json, "Positioning_with_Insight"),
            "Logic_with_Trust": self._extract_score(scoring_json, "Logic_with_Trust"),
            "Lead_with_Value": self._extract_score(scoring_json, "Lead_with_Value"),
        }

        dominant_pillar = max(pillar_scores, key=pillar_scores.get)
        weakest_pillar = min(pillar_scores, key=pillar_scores.get)
        sorted_pillars = sorted(pillar_scores.items(), key=lambda item: item[1], reverse=True)
        pillar_stack = [name for name, _ in sorted_pillars]

        awareness = pillar_scores["Awareness_with_Emotion"]
        insight = pillar_scores["Positioning_with_Insight"]
        trust = pillar_scores["Logic_with_Trust"]
        value = pillar_scores["Lead_with_Value"]

        is_balanced = (max(pillar_scores.values()) - min(pillar_scores.values())) <= 10

        if awareness >= 60 and trust < 50:
            permutation_strategy = "Emotional Authority Rebuild"
        elif insight >= 60 and value < 50:
            permutation_strategy = "Positioning Monetization Gap"
        elif trust >= 60 and awareness < 50:
            permutation_strategy = "Silent Authority Amplification"
        elif value >= 60 and insight < 50:
            permutation_strategy = "Offer Without Territory"
        elif is_balanced:
            permutation_strategy = "Integrated Growth Mode"
        else:
            permutation_strategy = "Structured Reinforcement Mode"

        strategic_focus = (
            f"Strengthen {weakest_pillar} while leveraging {dominant_pillar} "
            "to reduce structural imbalance."
        )

        return {
            "dominant_pillar": dominant_pillar,
            "weakest_pillar": weakest_pillar,
            "pillar_stack": pillar_stack,
            "permutation_strategy": permutation_strategy,
            "strategic_focus": strategic_focus,
        }

    def _extract_score(self, scoring_json, pillar_name):
        raw = scoring_json.get(pillar_name, 0)

        if isinstance(raw, dict):
            return float(raw.get("score", 0) or 0)

        return float(raw or 0)
