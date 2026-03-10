from openai import OpenAI
import os


class InstagramAlgorithmEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def rewrite_and_score(self, post_content, page_link):

        prompt = f"""
You are an Instagram performance strategist.

Analyze the post below using modern Instagram algorithm logic.

Check:
• Hook strength
• Retention probability
• Save potential
• Share potential
• Clarity
• Emotional pull

Then REWRITE and OPTIMIZE into:

Return ONLY JSON:

{{
"title":"",
"hook":"",
"body":"",
"cta":"",
"hashtags":[],
"alt_text":"",
"what_is_wrong":"",
"what_is_working":"",
"algorithm_score":"0-100"
}}

Post:
{post_content}

Page:
{page_link}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        return response.choices[0].message.content