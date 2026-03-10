import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class BrandIntelligenceEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze(self, brand_input, website_text, social_text):

        combined_text = f"""
WEBSITE CONTENT:
{website_text}

SOCIAL CONTENT:
{social_text}
"""

        prompt = f"""
You are a senior brand strategy analyst.

Analyze the brand below using website and social content.

Brand Name: {brand_input.brand_name}
Location: {brand_input.location}
Product/Service: {brand_input.product_service}
Current Problem: {brand_input.current_problem}
Brand Stage: {brand_input.brand_stage}

Content:
{combined_text}

IMPORTANT:

Choose ONLY ONE industry from this list:

• Creative Agency  
• Photography & Videography  
• Marketing & Advertising  
• Personal Brand  
• Education / Coaching  
• E-commerce  
• SaaS  
• Production House  

Rules:

1. Choose PRIMARY revenue driver only  
2. Ignore tone/style clues  
3. Base decision only on services + offerings  
4. If multiple apply → choose revenue core  
5. Never guess from visual storytelling language  

Extract structured JSON with these fields:

- industry
- business_model
- target_audience
- offer_clarity_score (1-10)
- tone
- value_proposition
- CTA_strength (1-10)
- trust_signals (list)
- strengths (list)
- weaknesses (list)
- diagnostic_summary (strategic overview)

Return ONLY valid JSON.
No explanation outside JSON.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior brand strategy analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,   # 🔥 LOCKED (VERY IMPORTANT)
        )

        import re
        import json

        content = response.choices[0].message.content.strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            result = json.loads(match.group(0))
        else:
            return content

        # -------------------------
        # HARD RULE OVERRIDE (STABILITY FIX)
        # -------------------------

        text_check = (website_text + social_text).lower()

        if any(word in text_check for word in ["wedding", "shoot", "studio", "cinematography", "photography"]):
            result["industry"] = "Photography & Videography"

        elif any(word in text_check for word in ["campaign", "strategy", "branding", "marketing", "ads"]):
            result["industry"] = "Creative Agency"

        return json.dumps(result)