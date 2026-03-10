import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class SEOIntelligenceEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze(self, website_text, primary_keyword=None, lifecycle_stage="Active"):
        current_year = datetime.now().year
        lifecycle_guidance = ""
        if lifecycle_stage == "Foundational":
            lifecycle_guidance = (
                "If brand is Foundational stage, prioritize content designed to establish "
                "topical authority and relevance rather than competitive ranking dominance. "
                "Focus on authority-building topics and problem-awareness content. Avoid "
                "competitive keyword domination strategy and aggressive ranking positioning."
            )

        prompt = f"""
You are an advanced SEO strategist.
Current year: {current_year}.
All recommendations must reflect forward-looking strategies for this year.
Do NOT reference outdated trends or past-year tactics.
Use present and emerging strategies only.

Analyze the following website content semantically.
This is NOT keyword density analysis.
Evaluate:

- Page structure quality
- Heading hierarchy clarity
- Semantic keyword usage
- Search intent match
- Content depth
- Blog/content consistency
- Overall ranking strength risk

Primary SEO keyword (if provided): {primary_keyword}
Lifecycle stage: {lifecycle_stage}
{lifecycle_guidance}

Temporal Awareness Rules:
- Assume this is {current_year}.
- Provide strategies that are relevant in this year and sustainable for the next 2-3 years.
- Avoid outdated algorithm assumptions.
- Focus on semantic search, intent modeling, AI-indexed search systems, and evolving discovery behavior.

Do not mention any year earlier than the current year.
Do not produce titles like 'Top Trends for 2023' or similar past references.
If examples are used, they must be relevant to the current year and beyond.

Return ONLY valid JSON in this format:

{{
  "seo_health_score": 0-100,
  "keyword_alignment": "Low / Medium / High",
  "intent_match_quality": "Poor / Moderate / Strong",
  "ranking_risk": "Low / Medium / High",
  "seo_weaknesses": [],
  "seo_topics": [
    {{
      "title": "",
      "intent_type": "",
      "content_angle": "",
      "why_relevant_now": ""
    }}
  ]
}}

Website Content:
{website_text[:12000]}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()

        # Extract clean JSON
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            return match.group(0)

        return content
