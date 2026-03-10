import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from intelligence.knowledge_layer import KnowledgeIntelligenceLayer

load_dotenv()


class AIExecutionEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.knowledge = KnowledgeIntelligenceLayer()

    def execute(self, brand_data, diagnosis_result, scoring_output, planning_output, lifecycle_stage="Active"):
        permutation_result = scoring_output.get("pillar_permutation", {}) if isinstance(scoring_output, dict) else {}
        dominant_pillar = permutation_result.get("dominant_pillar", "")
        weakest_pillar = permutation_result.get("weakest_pillar", "")
        permutation_guidance = {
            "dominant": dominant_pillar,
            "weakest": weakest_pillar,
            "reinforcement_action": self._reinforcement_action(weakest_pillar),
        }

        if lifecycle_stage == "Foundational":
            output = {
                "caption_variations": [
                    "Most growth problems are clarity problems. We fix clarity first.",
                    "If your audience cannot explain what you do, they will never buy.",
                    "We do not chase hacks. We build signal, authority, and trust.",
                    "Before scale, define your positioning. Everything else follows.",
                ],
                "hook_variations": [
                    "Unpopular take: content volume is overrated without positioning.",
                    "Hard truth: paid ads amplify confusion if your message is weak.",
                    "Most founders skip this one step and stall for months.",
                    "If your offer sounds like everyone else, the market ignores you.",
                ],
                "reel_scripts": [
                    {
                        "title": "Why Clarity Beats Volume",
                        "hook": "Posting more is not your problem.",
                        "script": "Explain how unclear positioning causes weak engagement, low trust, and inconsistent demand. Show one clear message framework founders can use this week.",
                        "cta": "Follow for clarity.",
                    },
                    {
                        "title": "The Mechanism Test",
                        "hook": "Can your audience repeat your method in one line?",
                        "script": "Break down category, problem, mechanism, and outcome in a quick educational format. Show how this improves authority signals.",
                        "cta": "Comment your view.",
                    },
                ],
                "carousel_breakdown": {
                    "title": "Positioning Clarity Framework",
                    "slides": [
                        "Slide 1: Why most brands stay invisible",
                        "Slide 2: Define your category",
                        "Slide 3: Name the core problem",
                        "Slide 4: Explain your mechanism",
                        "Slide 5: State the outcome clearly",
                        "Slide 6: CTA - DM to talk",
                    ],
                },
                "platform_specific_versions": {
                    "instagram": {
                        "content_focus": "Clarity + authority + engagement",
                        "recommended_formats": ["Reels", "Carousels", "Founder POV posts"],
                        "cta": "Follow for clarity",
                    }
                },
                "permutation_guidance": permutation_guidance,
            }
            return self._apply_weakest_pillar_reinforcement(output, weakest_pillar)

        primary_mode = diagnosis_result.get("primary_mode")
        risk_level = diagnosis_result.get("risk_level")
        framework = self.knowledge.get_framework()

        prompt = f"""
You are the EXECUTION LAYER of Brand Ark.

This output must be:
- Mode-driven
- State-driven
- Knowledge-influenced
- Four-Pillar aligned

Primary Mode: {primary_mode}
Risk Level: {risk_level}

Strategic Knowledge Framework:
{framework}

Pillar Permutation Guidance:
- Dominant pillar: {dominant_pillar}
- Weakest pillar: {weakest_pillar}
- Reinforcement action: {self._reinforcement_action(weakest_pillar)}

Execution Reinforcement Rules:
- If weakest pillar is Awareness_with_Emotion: increase hook strength and emotional contrast.
- If weakest pillar is Positioning_with_Insight: add category contrast lines in captions.
- If weakest pillar is Logic_with_Trust: add proof line in every output.
- If weakest pillar is Lead_with_Value: clarify benefit and CTA structure.

Return ONLY valid JSON:

{{
  "caption_variations": [
    {{"text": "", "score": 0-100}},
    {{"text": "", "score": 0-100}},
    {{"text": "", "score": 0-100}},
    {{"text": "", "score": 0-100}}
  ],
  "ad_variations": [
    {{"headline": "", "body": "", "cta": ""}},
    {{"headline": "", "body": "", "cta": ""}},
    {{"headline": "", "body": "", "cta": ""}},
    {{"headline": "", "body": "", "cta": ""}}
  ],
  "hook_variations": [
    "",
    "",
    "",
    ""
  ],
  "seo_optimized_version": "",
  "platform_specific_versions": {{
        "instagram": "",
        "linkedin": "",
        "x": "",
        "facebook": ""
  }}
}}

Brand Intelligence:
{brand_data}

Four Pillar Scores:
{scoring_output}

Planning Context:
{planning_output}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            try:
                output = json.loads(match.group(0))
                output["permutation_guidance"] = permutation_guidance
                return self._apply_weakest_pillar_reinforcement(output, weakest_pillar)
            except:
                return {"error": "Invalid JSON returned", "raw": content}

        return {"error": "No JSON detected", "raw": content}

    def _reinforcement_action(self, weakest_pillar):
        mapping = {
            "Awareness_with_Emotion": "Increase hook strength and emotional contrast.",
            "Positioning_with_Insight": "Add category contrast lines in captions.",
            "Logic_with_Trust": "Add proof line in every output.",
            "Lead_with_Value": "Clarify benefit and CTA structure.",
        }
        return mapping.get(weakest_pillar, "Use balanced reinforcement.")

    def _apply_weakest_pillar_reinforcement(self, output, weakest_pillar):
        patched = dict(output)

        if weakest_pillar == "Awareness_with_Emotion":
            hooks = patched.get("hook_variations", [])
            if isinstance(hooks, list):
                patched["hook_variations"] = [f"High-contrast angle: {hook}" for hook in hooks]

        if weakest_pillar == "Positioning_with_Insight":
            captions = patched.get("caption_variations", [])
            if isinstance(captions, list):
                updated = []
                for caption in captions:
                    if isinstance(caption, dict):
                        text = caption.get("text", "")
                        caption["text"] = f"{text} Category contrast: not generic marketing, but strategic positioning."
                        updated.append(caption)
                    else:
                        updated.append(
                            f"{caption} Category contrast: not generic marketing, but strategic positioning."
                        )
                patched["caption_variations"] = updated

        if weakest_pillar == "Logic_with_Trust":
            captions = patched.get("caption_variations", [])
            if isinstance(captions, list):
                updated = []
                for caption in captions:
                    if isinstance(caption, dict):
                        text = caption.get("text", "")
                        caption["text"] = f"{text} Proof: method validated through repeatable outcomes."
                        updated.append(caption)
                    else:
                        updated.append(f"{caption} Proof: method validated through repeatable outcomes.")
                patched["caption_variations"] = updated

        if weakest_pillar == "Lead_with_Value":
            captions = patched.get("caption_variations", [])
            if isinstance(captions, list):
                updated = []
                for caption in captions:
                    if isinstance(caption, dict):
                        text = caption.get("text", "")
                        caption["text"] = f"{text} Benefit: faster clarity and stronger conversion. CTA: DM to talk."
                        updated.append(caption)
                    else:
                        updated.append(
                            f"{caption} Benefit: faster clarity and stronger conversion. CTA: DM to talk."
                        )
                patched["caption_variations"] = updated

        return patched
