from strategy.foundation_strategy import FoundationStrategyPath


class StrategyBrain:

    def __init__(self, diagnosis_result, lifecycle_stage="Active"):
        self.mode = diagnosis_result.get("primary_mode")
        self.risk_level = diagnosis_result.get("risk_level")
        self.lifecycle_stage = lifecycle_stage
        self.demand_status = diagnosis_result.get("demand_validation", {}).get("demand_status")

    # =========================
    # 90 DAY CAMPAIGN ARC
    # =========================

    def generate_90_day_arc(self):
        if self.lifecycle_stage == "Foundational" or self.demand_status == "Premature":
            return FoundationStrategyPath().generate()
        if self.demand_status in ["Weak", "Unclear"]:
            return {
                "phase": "Demand Validation Realignment",
                "focus": [
                    "Problem clarity",
                    "Market testing",
                    "Offer articulation",
                    "Audience validation loops",
                ],
                "weekly_structure": {
                    "problem_clarity_posts": 3,
                    "market_test_posts": 2,
                    "offer_articulation_posts": 1,
                    "audience_feedback_loop_posts": 1,
                },
            }

        if self.mode == "Emergency Rebuild":
            return [
                {"month": 1, "focus": "Structural Reset", "goal": "Clarify positioning + rebuild trust"},
                {"month": 2, "focus": "Re-Alignment", "goal": "Reintroduce offer with authority"},
                {"month": 3, "focus": "Controlled Relaunch", "goal": "Stabilize demand signals"}
            ]

        if self.mode == "Reposition":
            return [
                {"month": 1, "focus": "Positioning Clarity", "goal": "Differentiate strongly"},
                {"month": 2, "focus": "Authority Building", "goal": "Insight-led content"},
                {"month": 3, "focus": "Conversion Strengthening", "goal": "Improve value articulation"}
            ]

        if self.mode == "Stabilize":
            return [
                {"month": 1, "focus": "Trust Layer Strengthening", "goal": "Case studies + testimonials"},
                {"month": 2, "focus": "Conversion Optimization", "goal": "Improve CTA + landing clarity"},
                {"month": 3, "focus": "Efficiency Improvement", "goal": "Lower CAC, increase ROAS"}
            ]

        if self.mode == "Optimize":
            return [
                {"month": 1, "focus": "Funnel Optimization", "goal": "Improve conversion stages"},
                {"month": 2, "focus": "Audience Refinement", "goal": "Improve targeting precision"},
                {"month": 3, "focus": "Scaling Preparation", "goal": "Strengthen retention systems"}
            ]

        if self.mode == "Scale":
            return [
                {"month": 1, "focus": "Aggressive Media Expansion", "goal": "Increase acquisition volume"},
                {"month": 2, "focus": "Market Expansion", "goal": "New segments / geo expansion"},
                {"month": 3, "focus": "Authority Domination", "goal": "Category leadership positioning"}
            ]

        return []


    # =========================
    # BUDGET ALLOCATION MODEL
    # =========================

    def budget_model(self, monthly_budget):
        if self.lifecycle_stage == "Foundational" or self.demand_status in ["Weak", "Unclear", "Premature"]:
            return {}

        if self.mode == "Emergency Rebuild":
            return {
                "brand_clarity": 40,
                "content_foundation": 30,
                "paid_ads": 20,
                "tools_and_tracking": 10
            }

        if self.mode == "Reposition":
            return {
                "content_strategy": 35,
                "authority_content": 30,
                "paid_testing": 25,
                "tools": 10
            }

        if self.mode == "Stabilize":
            return {
                "conversion_assets": 30,
                "retargeting_ads": 35,
                "content": 25,
                "optimization_tools": 10
            }

        if self.mode == "Optimize":
            return {
                "performance_ads": 45,
                "conversion_rate_optimization": 25,
                "retention": 20,
                "tools": 10
            }

        if self.mode == "Scale":
            return {
                "media_buying": 60,
                "brand_building": 20,
                "automation": 10,
                "innovation_testing": 10
            }

        return {}


    # =========================
    # MEDIA MIX SPLIT
    # =========================

    def media_mix(self):

        if self.mode in ["Emergency Rebuild", "Reposition"]:
            return {
                "organic": 60,
                "paid": 30,
                "experimental": 10
            }

        if self.mode == "Stabilize":
            return {
                "organic": 40,
                "paid": 50,
                "experimental": 10
            }

        if self.mode == "Optimize":
            return {
                "organic": 30,
                "paid": 60,
                "experimental": 10
            }

        if self.mode == "Scale":
            return {
                "organic": 20,
                "paid": 70,
                "experimental": 10
            }

        return {}


    # =========================
    # RISK MODELING
    # =========================

    def risk_model(self):

        if self.risk_level in ["Critical", "High"]:
            return {
                "priority": "Stability first",
                "action": "Reduce aggressive scaling",
                "monitoring": "Weekly performance audit"
            }

        if self.risk_level == "Medium":
            return {
                "priority": "Balanced growth",
                "action": "Test before scale",
                "monitoring": "Bi-weekly review"
            }

        return {
            "priority": "Growth expansion",
            "action": "Increase acquisition pressure",
            "monitoring": "Monthly performance review"
        }


    # =========================
    # SCALING THRESHOLDS
    # =========================

    def scaling_thresholds(self):
        if self.lifecycle_stage == "Foundational" or self.demand_status in ["Weak", "Unclear", "Premature"]:
            return {}

        return {
            "min_roas_for_scale": 3.0,
            "min_conversion_rate": 2.5,
            "max_cac_growth": "10%",
            "retention_threshold": "25%"
        }


    # =========================
    # OPTIMIZATION LOOP
    # =========================

    def optimization_loop(self):
        if self.lifecycle_stage == "Foundational" or self.demand_status in ["Weak", "Unclear", "Premature"]:
            return {}

        return {
            "analyze": "Weekly performance data review",
            "diagnose": "Identify funnel bottleneck",
            "adjust": "Creative + targeting refinement",
            "scale": "Increase budget on validated assets"
        }

    # =========================
    # FOUNDATIONAL CALENDAR
    # =========================

    def generate_foundational_30_day_calendar(self, brand_name, brand_data):

        if self.lifecycle_stage != "Foundational":
            return []

        industry = brand_data.get("industry", "your category")
        audience = brand_data.get("target_audience", "your ideal audience")
        value_prop = brand_data.get("value_proposition", "your core value")
        tone = brand_data.get("tone", "clear, helpful tone")
        brand_label = brand_name or "Your Brand"

        formats = [
            "Reel",
            "Carousel",
            "Single Image",
            "Story Series",
            "Text Post",
        ]

        idea_templates = [
            {
                "theme": "Founder Story",
                "idea": "Why {brand} started in {industry} and what problem it solves for {audience}.",
                "cta": "Comment with your biggest challenge.",
            },
            {
                "theme": "Problem Breakdown",
                "idea": "Top 3 mistakes people make in {industry} and how to avoid them.",
                "cta": "Save this for later.",
            },
            {
                "theme": "Value Proposition",
                "idea": "What makes {brand} different: {value_prop}.",
                "cta": "Share this with someone who needs it.",
            },
            {
                "theme": "Quick Education",
                "idea": "Explain one practical concept your audience can apply today.",
                "cta": "Tell us if you want part 2.",
            },
            {
                "theme": "Myth vs Reality",
                "idea": "Debunk one common myth in {industry} for {audience}.",
                "cta": "Drop a myth you want us to break next.",
            },
            {
                "theme": "Behind the Scenes",
                "idea": "Show how {brand} builds quality and trust day to day.",
                "cta": "Ask anything about the process.",
            },
            {
                "theme": "Trust Asset",
                "idea": "Share a mini case example: challenge, action, result.",
                "cta": "DM us to see if this fits your situation.",
            },
            {
                "theme": "Offer Clarity",
                "idea": "Break down what you offer, who it is for, and expected outcome.",
                "cta": "Reply with 'guide' for details.",
            },
            {
                "theme": "Objection Handling",
                "idea": "Address the top hesitation your audience has before buying.",
                "cta": "Comment your hesitation and we will answer.",
            },
            {
                "theme": "Community Prompt",
                "idea": "Post an opinion question relevant to {audience} in {industry}.",
                "cta": "Vote in comments and explain why.",
            },
        ]

        calendar = []

        for day in range(1, 31):
            template = idea_templates[(day - 1) % len(idea_templates)]
            content_format = formats[(day - 1) % len(formats)]

            calendar.append(
                {
                    "day": day,
                    "format": content_format,
                    "theme": template["theme"],
                    "idea": template["idea"].format(
                        brand=brand_label,
                        industry=industry,
                        audience=audience,
                        value_prop=value_prop,
                    ),
                    "tone": tone,
                    "objective": "Build baseline signal, clarity, and trust.",
                    "cta": template["cta"],
                }
            )

        return calendar

    def generate_simple_flow(self, diagnosis):

        return [
            {
                "month": "Month 1 — Awareness + Narrative",
                "tasks": [
                    "Fix positioning clarity",
                    "Build emotional storytelling",
                    "Define narrative tone",
                    "Create trust foundation"
                ],
                "weekly_plan": [
                    {
                        "week": 1,
                        "posts": [
                            "Brand story introduction",
                            "Founder POV",
                            "Problem awareness carousel"
                        ]
                    },
                    {
                        "week": 2,
                        "posts": [
                            "Audience pain breakdown",
                            "Relatable storytelling reel",
                            "Educational insight post"
                        ]
                    },
                    {
                        "week": 3,
                        "posts": [
                            "Case-style storytelling",
                            "Contrarian POV reel",
                            "Audience myth-busting"
                       ]
                    },
                    {
                        "week": 4,
                        "posts": [
                            "Emotional narrative reel",
                            "Trust-building insight",
                            "Soft CTA content"
                       ]
                   }
                ]
            },
            {
                "month": "Month 2 — Authority + Trust",
                "tasks": [
                    "Build authority positioning",
                    "Add testimonials",
                    "Strengthen logical messaging"
                ],
                "weekly_plan": [
                    {"week": 1, "posts": ["Framework breakdown", "Process video", "Case post"]},
                    {"week": 2, "posts": ["Testimonial", "Before-after story", "Expert insight"]},
                    {"week": 3, "posts": ["Deep educational", "Authority POV", "Live clip"]},
                    {"week": 4, "posts": ["FAQ reel", "Trust CTA", "Conversion education"]}
                ]
            },
            {
                "month": "Month 3 — Conversion + Ad Film",
                "tasks": [
                    "Shift messaging toward conversion",
                    "Plan ad film narrative",
                    "Execute production + launch"
                ],
                "weekly_plan": [
                    {"week": 1, "posts": ["Offer clarity", "Proof content", "Conversion reel"]},
                    {"week": 2, "posts": ["Ad film teaser", "Problem hook", "Authority CTA"]},
                    {"week": 3, "posts": ["Behind scenes", "Story-driven post", "CTA reel"]},
                    {"week": 4, "posts": ["Ad film launch", "Retarget reel", "Strong CTA"]}
                ]
            }
        ]