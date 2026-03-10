class PillarInteractionEngine:

    def analyze(self, scores):

        A = scores["Awareness_with_Emotion"]["score"]
        P = scores["Positioning_with_Insight"]["score"]
        T = scores["Logic_with_Trust"]["score"]
        V = scores["Lead_with_Value"]["score"]

        patterns = []

        if A > 70 and T < 40:
            patterns.append("High Awareness but Low Trust → Viral but low conversion risk.")

        if P > 70 and V < 40:
            patterns.append("Strong Insight but Weak Value → Smart positioning, poor monetization.")

        if T > 70 and A < 40:
            patterns.append("Strong Trust but Low Visibility → Hidden authority.")

        if V > 70 and P < 40:
            patterns.append("Strong Offer but Weak Positioning → Commodity perception risk.")

        if A > 70 and P > 70 and T > 70 and V > 70:
            patterns.append("Pillar Alignment High → Brand Dominance Potential.")

        imbalance_index = max(A, P, T, V) - min(A, P, T, V)

        return {
            "pillar_patterns": patterns,
            "imbalance_index": imbalance_index
        }