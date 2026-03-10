import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from intelligence.knowledge_layer import KnowledgeIntelligenceLayer
from intelligence.pillar_permutation_engine import PillarPermutationEngine

load_dotenv()


class AIIntelligenceScoringEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.knowledge = KnowledgeIntelligenceLayer()
        self.permutation_engine = PillarPermutationEngine()

    def evaluate(self, brand_data):

        framework = self.knowledge.get_framework()

        prompt = f"""
You are evaluating a brand using FOUR STRATEGIC PILLARS.

The pillars are:

1. Awareness with Emotion
2. Positioning with Insight
3. Logic with Trust
4. Lead with Value

Use the following philosophical standards to guide evaluation:

{framework}

Return ONLY valid JSON:

{{
  "Awareness_with_Emotion": {{
      "score": 0-100,
      "reason": ""
  }},
  "Positioning_with_Insight": {{
      "score": 0-100,
      "reason": ""
  }},
  "Logic_with_Trust": {{
      "score": 0-100,
      "reason": ""
  }},
  "Lead_with_Value": {{
      "score": 0-100,
      "reason": ""
  }}
}}

Brand Data:
{brand_data}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.dumps(json.loads(content))
        except:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.dumps(json.loads(match.group(0)))

        return content
