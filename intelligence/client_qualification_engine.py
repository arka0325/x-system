# intelligence/client_qualification_engine.py

class ClientQualificationEngine:

    def __init__(self):
        pass

    def evaluate(
        self,
        brand_intelligence,
        diagnosis,
        demand_validation,
        lifecycle_stage,
        monthly_budget=0,
        urgency_level="Medium",
    ):

        # ----------------------------
        # 1. Strategic Fit (25)
        # ----------------------------
        strategic_fit_score = 0

        demand_status = demand_validation.get("demand_status")

        if demand_status == "Validated":
            strategic_fit_score = 25
        elif demand_status == "Unclear":
            strategic_fit_score = 15
        elif demand_status == "Weak":
            strategic_fit_score = 10
        else:  # Premature / Foundational
            strategic_fit_score = 8

        # ----------------------------
        # 2. Budget Fit (20)
        # ----------------------------
        budget_fit_score = 0

        if monthly_budget >= 150000:
            budget_fit_score = 20
        elif monthly_budget >= 75000:
            budget_fit_score = 15
        elif monthly_budget >= 40000:
            budget_fit_score = 10
        else:
            budget_fit_score = 5

        # ----------------------------
        # 3. Execution Readiness (20)
        # ----------------------------
        execution_readiness_score = 0

        offer_clarity = brand_intelligence.get("offer_clarity_score", 5)

        if lifecycle_stage == "Active" and offer_clarity >= 7:
            execution_readiness_score = 20
        elif offer_clarity >= 5:
            execution_readiness_score = 14
        else:
            execution_readiness_score = 8

        # ----------------------------
        # 4. Expectation Alignment (20)
        # ----------------------------
        expectation_alignment_score = 15

        if urgency_level == "High":
            expectation_alignment_score = 10

        # ----------------------------
        # 5. Risk Score (15)
        # ----------------------------
        risk_score = 10
        risk_flags = []

        if demand_status in ["Weak", "Unclear"]:
            risk_flags.append("Demand not fully validated")

        if offer_clarity < 5:
            risk_flags.append("Low offer clarity")

        if monthly_budget < 40000:
            risk_flags.append("Low execution budget")

        if urgency_level == "High":
            risk_flags.append("High urgency expectation")

        if len(risk_flags) >= 3:
            risk_score = 5

        # ----------------------------
        # FINAL SCORE
        # ----------------------------
        qualification_score = (
            strategic_fit_score
            + budget_fit_score
            + execution_readiness_score
            + expectation_alignment_score
            + risk_score
        )

        # ----------------------------
        # STATUS LOGIC
        # ----------------------------
        if qualification_score >= 75:
            qualification_status = "Accept"
        elif qualification_score >= 55:
            qualification_status = "Conditional"
        else:
            qualification_status = "Reject"

        # ----------------------------
        # ENGAGEMENT MODEL
        # ----------------------------
        if lifecycle_stage == "Foundational":
            engagement_model = "Foundation Build Program"

        elif demand_status == "Validated":
            engagement_model = "Growth Acceleration"

        else:
            engagement_model = "Strategy Reset Sprint"

        # ----------------------------
        # SUMMARY
        # ----------------------------
        recommendation_summary = (
            f"Client scored {qualification_score}. Status: {qualification_status}. "
            f"Recommended engagement: {engagement_model}."
        )

        return {
            "qualification_score": qualification_score,
            "qualification_status": qualification_status,
            "strategic_fit_score": strategic_fit_score,
            "budget_fit_score": budget_fit_score,
            "execution_readiness_score": execution_readiness_score,
            "expectation_alignment_score": expectation_alignment_score,
            "risk_score": risk_score,
            "risk_flags": risk_flags,
            "engagement_model": engagement_model,
            "recommendation_summary": recommendation_summary,
        }
       