import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OptimizationEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def evaluate(self, metrics, diagnosis_result):

        ctr = metrics.get("ctr")
        roas = metrics.get("roas")
        cpc = metrics.get("cpc")
        conversion_rate = metrics.get("conversion_rate")

        # =========================
        # RULE SIGNAL DETECTION
        # =========================

        signals = {
            "low_ctr": ctr < 1.0,
            "low_roas": roas < 2.0,
            "high_cpc": cpc > 80,
            "low_conversion": conversion_rate < 1.5
        }

        prompt = f"""
You are the Optimization Layer of Brand Ark.

Performance Metrics:
CTR: {ctr}
ROAS: {roas}
CPC: {cpc}
Conversion Rate: {conversion_rate}

Current Mode:
{diagnosis_result.get("primary_mode")}

Signals Detected:
{signals}

Return ONLY valid JSON:

{{
  "performance_health": "Strong | Moderate | Weak | Critical",
  "rewrite_trigger": [],
  "budget_shift": "",
  "mode_shift": "",
  "strategic_adjustment": "",
  "reasoning": ""
}}

Rules Context:
- Low CTR usually means hook weakness.
- Low ROAS suggests value or conversion issue.
- High CPC may indicate audience misalignment.
- Low conversion suggests offer clarity or trust gap.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            try:
                return json.loads(match.group(0))
            except:
                return {"error": "Invalid JSON returned", "raw": content}

        return {"error": "No JSON detected", "raw": content}