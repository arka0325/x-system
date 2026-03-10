class DemandValidationGate:

    def evaluate(
        self,
        brand_intelligence,
        seo_intelligence,
        pillar_scores,
        lifecycle_stage,
        engagement_signals=None,
    ):
        if lifecycle_stage == "Foundational":
            return {
                "demand_status": "Premature",
                "demand_strength_score": None,
                "problem_market_fit": "Not Applicable",
                "offer_market_alignment": "Not Applicable",
                "risk_flag": "Validation Deferred",
                "strategic_implication": "Signal building required before demand validation",
            }

        keyword_alignment = str(seo_intelligence.get("keyword_alignment", "")).strip().lower()
        intent_match = str(seo_intelligence.get("intent_match_quality", "")).strip().lower()
        offer_clarity = self._normalize_offer_clarity(brand_intelligence.get("offer_clarity_score"))
        problem_defined = self._is_problem_defined(brand_intelligence)

        if keyword_alignment == "low" and offer_clarity < 50:
            demand_status = "Weak"
        elif problem_defined and intent_match == "strong":
            demand_status = "Validated"
        else:
            demand_status = "Unclear"

        demand_strength_score = self._calculate_demand_strength(
            keyword_alignment=keyword_alignment,
            intent_match=intent_match,
            offer_clarity=offer_clarity,
            pillar_scores=pillar_scores,
            engagement_signals=engagement_signals or {},
        )

        problem_market_fit = self._problem_market_fit(problem_defined, intent_match)
        offer_market_alignment = self._offer_market_alignment(offer_clarity)
        risk_flag = self._risk_flag(demand_status)
        strategic_implication = self._strategic_implication(demand_status)

        return {
            "demand_status": demand_status,
            "demand_strength_score": demand_strength_score,
            "problem_market_fit": problem_market_fit,
            "offer_market_alignment": offer_market_alignment,
            "risk_flag": risk_flag,
            "strategic_implication": strategic_implication,
        }

    def _normalize_offer_clarity(self, value):
        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.0

        if score <= 10:
            return max(0.0, min(score * 10.0, 100.0))
        return max(0.0, min(score, 100.0))

    def _is_problem_defined(self, brand_intelligence):
        current_problem = str(brand_intelligence.get("current_problem", "")).strip()
        diagnostic_summary = str(brand_intelligence.get("diagnostic_summary", "")).lower()
        weaknesses = brand_intelligence.get("weaknesses", [])

        if current_problem:
            return True
        if "problem" in diagnostic_summary:
            return True
        return isinstance(weaknesses, list) and len(weaknesses) > 0

    def _pillar_average(self, pillar_scores):
        keys = [
            "Awareness_with_Emotion",
            "Positioning_with_Insight",
            "Logic_with_Trust",
            "Lead_with_Value",
        ]
        values = []
        for key in keys:
            raw = pillar_scores.get(key, {})
            if isinstance(raw, dict):
                values.append(float(raw.get("score", 0) or 0))
            else:
                values.append(float(raw or 0))
        return sum(values) / len(values)

    def _calculate_demand_strength(
        self,
        keyword_alignment,
        intent_match,
        offer_clarity,
        pillar_scores,
        engagement_signals,
    ):
        keyword_map = {"low": 30, "medium": 60, "high": 85}
        intent_map = {"poor": 30, "moderate": 60, "strong": 85}

        keyword_score = keyword_map.get(keyword_alignment, 45)
        intent_score = intent_map.get(intent_match, 45)
        pillar_score = self._pillar_average(pillar_scores)
        engagement_score = self._engagement_score(engagement_signals)

        strength = (
            (0.25 * keyword_score)
            + (0.30 * intent_score)
            + (0.25 * offer_clarity)
            + (0.15 * pillar_score)
            + (0.05 * engagement_score)
        )
        return round(max(0.0, min(strength, 100.0)), 2)

    def _engagement_score(self, engagement_signals):
        if not isinstance(engagement_signals, dict) or not engagement_signals:
            return 50.0

        ctr = float(engagement_signals.get("ctr", 1.0) or 1.0)
        conversion = float(engagement_signals.get("conversion_rate", 1.0) or 1.0)
        score = (min(ctr, 5.0) / 5.0) * 50 + (min(conversion, 5.0) / 5.0) * 50
        return round(score, 2)

    def _problem_market_fit(self, problem_defined, intent_match):
        if problem_defined and intent_match == "strong":
            return "Strong"
        if problem_defined or intent_match == "moderate":
            return "Moderate"
        return "Weak"

    def _offer_market_alignment(self, offer_clarity):
        if offer_clarity >= 70:
            return "Strong"
        if offer_clarity >= 50:
            return "Moderate"
        return "Weak"

    def _risk_flag(self, demand_status):
        mapping = {
            "Validated": "Low Risk",
            "Unclear": "Moderate Risk",
            "Weak": "High Risk",
            "Premature": "Validation Deferred",
        }
        return mapping.get(demand_status, "Moderate Risk")

    def _strategic_implication(self, demand_status):
        mapping = {
            "Validated": "Demand signal confirmed. Controlled growth can proceed.",
            "Unclear": "Mixed demand signals. Run structured demand testing before scaling.",
            "Weak": "Demand weak. Reposition offer and sharpen problem-market narrative.",
            "Premature": "Signal building required before demand validation",
        }
        return mapping.get(demand_status, "Collect more demand evidence before major scaling decisions.")
