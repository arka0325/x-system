import os
import json
import re
import math
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIPlanningEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_plan(self, brand_data, diagnosis_result, scoring_output, lifecycle_stage="Active"):
        permutation_result = scoring_output.get("pillar_permutation", {}) if isinstance(scoring_output, dict) else {}
        dominant_pillar = permutation_result.get("dominant_pillar")
        weakest_pillar = permutation_result.get("weakest_pillar")

        if lifecycle_stage == "Foundational":
            plan = {
                "weekly_content_themes": [
                    "Positioning clarity",
                    "Problem agitation",
                    "Mechanism explanation",
                    "Founder POV",
                ],
                "story_angles": [
                    "Why most marketing advice fails",
                    "What ArkX stands for",
                    "Behind the system",
                    "Myth busting in marketing",
                ],
                "hook_bank": [
                    "Most brands are not broken, they are unclear.",
                    "Growth is not a traffic issue, it is a positioning issue.",
                    "If everyone understands your offer, nobody remembers it.",
                    "The market does not reward effort, it rewards clarity.",
                    "Consistency without strategy is just noise.",
                    "More content will not fix a weak narrative.",
                    "Your audience is not confused, your message is.",
                    "Virality cannot save a brand with no point of view.",
                    "Brand trust is built before paid ads start.",
                    "Most funnels fail at the first sentence.",
                    "You do not need more hacks, you need one clear mechanism.",
                    "Authority starts when you say what you stand against.",
                ],
                "cta_mapping": {
                    "awareness": "Follow for clarity",
                    "engagement": "Comment your view",
                    "conversion": "DM to talk",
                },
            }
            return self._ensure_weakest_pillar_reinforcement(plan, weakest_pillar)

        primary_mode = diagnosis_result.get("primary_mode")
        strategic_priority = diagnosis_result.get("strategic_priority")

        prompt = f"""
You are the Planning Layer of Brand Ark.

You generate execution plan aligned with:
- Brand Intelligence
- Four Pillar Scores
- Diagnosis Mode
- Strategic Priority

Primary Mode: {primary_mode}
Strategic Priority: {strategic_priority}
Dominant Pillar: {dominant_pillar}
Weakest Pillar: {weakest_pillar}

Pillar Prioritization Rules:
{self._dominant_pillar_instruction(dominant_pillar)}
If weakest pillar exists, at least 30% of weekly content themes must reinforce {weakest_pillar}.

Return ONLY valid JSON:

{{
  "weekly_content_themes": [],
  "story_angles": [],
  "hook_bank": [],
  "ad_ideas": [],
  "seo_topics": [],
  "reel_scripts": [],
  "carousel_breakdowns": [],
  "cta_mapping": {{
        "awareness": "",
        "consideration": "",
        "conversion": ""
  }},
  "hook_testing_protocol": {{
        "variants_per_hook": "",
        "testing_window_days": "",
        "decision_metric": ""
  }}
}}

Brand Intelligence:
{brand_data}

Four Pillar Scores:
{scoring_output}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            try:
                plan = json.loads(match.group(0))
                return self._ensure_weakest_pillar_reinforcement(plan, weakest_pillar)
            except:
                return {"error": "Invalid JSON returned", "raw": content}

        return {"error": "No JSON detected", "raw": content}

    def _dominant_pillar_instruction(self, dominant_pillar):
        mapping = {
            "Awareness_with_Emotion": "Weekly themes must prioritize emotion-led storytelling.",
            "Positioning_with_Insight": "Weekly themes must prioritize differentiation and thought leadership.",
            "Logic_with_Trust": "Weekly themes must prioritize proof, case studies, and breakdowns.",
            "Lead_with_Value": "Weekly themes must prioritize offer clarity and outcome visibility.",
        }
        return mapping.get(dominant_pillar, "Use balanced theme prioritization.")

    def _reinforcement_theme(self, weakest_pillar):
        mapping = {
            "Awareness_with_Emotion": "Emotional hook reinforcement and audience resonance",
            "Positioning_with_Insight": "Category contrast and positioning reinforcement",
            "Logic_with_Trust": "Proof reinforcement through outcomes and trust signals",
            "Lead_with_Value": "Offer clarity and value articulation reinforcement",
        }
        return mapping.get(weakest_pillar, "")

    def _ensure_weakest_pillar_reinforcement(self, plan, weakest_pillar):
        output = dict(plan)
        themes = output.get("weekly_content_themes")
        reinforcement_theme = self._reinforcement_theme(weakest_pillar)

        if not isinstance(themes, list) or not themes or not reinforcement_theme:
            return output

        required = math.ceil(len(themes) * 0.3)
        current = sum(1 for theme in themes if reinforcement_theme.lower() in str(theme).lower())

        while current < required:
            themes.append(reinforcement_theme)
            current += 1

        output["weekly_content_themes"] = themes
        return output
