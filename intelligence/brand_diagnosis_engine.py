import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from intelligence.knowledge_layer import KnowledgeIntelligenceLayer
from intelligence.demand_validation_engine import DemandValidationGate

load_dotenv()


class BrandDiagnosisEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.knowledge = KnowledgeIntelligenceLayer()
        self.demand_gate = DemandValidationGate()

    def diagnose(self, brand_intelligence, seo_intelligence, scoring_output):
        lifecycle_stage = brand_intelligence.get("lifecycle_stage", "Active")
        permutation_result = scoring_output.get("pillar_permutation", {})
        weakest_score = self._pillar_score(scoring_output, permutation_result.get("weakest_pillar"))
        dominant_score = self._pillar_score(scoring_output, permutation_result.get("dominant_pillar"))
        is_balanced = self._is_balanced_structure(scoring_output, permutation_result)
        demand_result = self.demand_gate.evaluate(
            brand_intelligence=brand_intelligence,
            seo_intelligence=seo_intelligence,
            pillar_scores=scoring_output,
            lifecycle_stage=lifecycle_stage,
        )
        pillar_strength = self._pillar_average(scoring_output)

        if lifecycle_stage == "Foundational":
            base_result = {
                "primary_mode": "Build",
                "secondary_mode": None,
                "strategic_priority": "Signal Building and Identity Clarity",
                "risk_level": "Low",
                "immediate_actions": [
                    "Clarify positioning",
                    "Publish 12–15 foundational posts",
                    "Introduce founder voice",
                    "Build first trust assets"
                ],
                "reasoning": "Brand is in foundational stage. Scaling and optimization disabled."
            }
            return self._apply_permutation_rules(
                diagnosis_result=base_result,
                permutation_result=permutation_result,
                weakest_score=weakest_score,
                dominant_score=dominant_score,
                is_balanced=is_balanced,
                demand_result=demand_result,
                pillar_strength=pillar_strength,
            )

        framework = self.knowledge.get_framework()

        prompt = f"""
You are the strategic decision core of Brand Ark.

You must determine the correct operating mode of a brand.

You are influenced by:

1. Brand Intelligence Data
2. SEO Intelligence Data
3. Four Pillar Scoring
4. Strategic Knowledge Framework

Strategic Knowledge Framework:
{framework}

Lifecycle Stage:
{lifecycle_stage}

Pillar Permutation:
{permutation_result}

Demand Validation:
{demand_result}

Available Modes:
- Reposition
- Stabilize
- Optimize
- Scale
- Emergency Rebuild

Mode Definitions:

Reposition:
Brand message unclear, positioning weak, moderate foundation.

Stabilize:
Some traction exists but inconsistent structure and clarity.

Optimize:
Strong structure but inefficiencies in conversion or demand capture.

Scale:
High clarity, strong trust, strong value perception, ready for expansion.

Emergency Rebuild:
Severe clarity, trust, or value collapse. Structural reset required.

Return ONLY valid JSON:

{{
  "primary_mode": "",
  "secondary_mode": "",
  "strategic_priority": "",
  "risk_level": "Low | Medium | High | Critical",
  "immediate_actions": [],
  "reasoning": ""
}}

Brand Intelligence:
{brand_intelligence}

SEO Intelligence:
{seo_intelligence}

Four Pillar Scores:
{scoring_output}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            try:
                ai_result = json.loads(match.group(0))
                return self._apply_permutation_rules(
                    diagnosis_result=ai_result,
                    permutation_result=permutation_result,
                    weakest_score=weakest_score,
                    dominant_score=dominant_score,
                    is_balanced=is_balanced,
                    demand_result=demand_result,
                    pillar_strength=pillar_strength,
                )
            except:
                return {"error": "Invalid JSON returned", "raw": content}

        return {"error": "No JSON detected", "raw": content}

    def _apply_permutation_rules(
        self,
        diagnosis_result,
        permutation_result,
        weakest_score,
        dominant_score,
        is_balanced,
        demand_result,
        pillar_strength,
    ):
        output = dict(diagnosis_result)
        demand_status = demand_result.get("demand_status")

        if demand_status == "Premature":
            output["primary_mode"] = "Foundation Build"
        elif demand_status == "Weak":
            output["primary_mode"] = "Reposition"
        elif demand_status == "Unclear":
            output["primary_mode"] = "Stabilize"
        elif demand_status == "Validated" and pillar_strength >= 70:
            pass
        elif demand_status == "Validated" and output.get("primary_mode") in ["Optimize", "Scale"]:
            output["primary_mode"] = "Stabilize"

        if weakest_score is not None and weakest_score < 40:
            output["risk_level"] = self._increase_risk_tier(output.get("risk_level", "Low"))

        if (
            demand_status != "Premature"
            and dominant_score is not None
            and weakest_score is not None
            and dominant_score > 75
            and weakest_score < 40
        ):
            output["strategic_priority"] = "Reinforce Structural Imbalance"
        elif demand_status != "Premature" and is_balanced:
            output["strategic_priority"] = "Layered Expansion"

        output["pillar_permutation"] = permutation_result
        output["demand_validation"] = demand_result
        return output

    def _increase_risk_tier(self, current_risk):
        tiers = ["Low", "Medium", "High", "Critical"]
        if current_risk not in tiers:
            return "Medium"

        idx = tiers.index(current_risk)
        return tiers[min(idx + 1, len(tiers) - 1)]

    def _pillar_score(self, scoring_output, pillar_name):
        if not pillar_name:
            return None

        pillar_data = scoring_output.get(pillar_name, {})
        if isinstance(pillar_data, dict):
            return float(pillar_data.get("score", 0) or 0)

        return float(pillar_data or 0)

    def _is_balanced_structure(self, scoring_output, permutation_result):
        if permutation_result.get("permutation_strategy") == "Integrated Growth Mode":
            return True

        pillars = [
            "Awareness_with_Emotion",
            "Positioning_with_Insight",
            "Logic_with_Trust",
            "Lead_with_Value",
        ]
        scores = [self._pillar_score(scoring_output, pillar) for pillar in pillars]
        return (max(scores) - min(scores)) <= 10

    def _pillar_average(self, scoring_output):
        pillars = [
            "Awareness_with_Emotion",
            "Positioning_with_Insight",
            "Logic_with_Trust",
            "Lead_with_Value",
        ]
        scores = [self._pillar_score(scoring_output, pillar) or 0 for pillar in pillars]
        return sum(scores) / len(scores)
