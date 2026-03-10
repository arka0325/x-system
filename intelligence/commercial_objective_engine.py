# intelligence/commercial_objective_engine.py

class CommercialObjectiveEngine:

    def __init__(self):
        pass

    def lock(
        self,
        lifecycle_stage,
        diagnosis,
        client_goal,
        monthly_budget,
        urgency_level
    ):

        # -------------------------
        # PRIMARY OBJECTIVE LOGIC
        # -------------------------

        if lifecycle_stage == "Foundational":
            primary_objective = "Attention + Signal Building"

        else:
            if "lead" in client_goal.lower():
                primary_objective = "Lead Generation"

            elif "sales" in client_goal.lower():
                primary_objective = "Revenue Growth"

            elif "awareness" in client_goal.lower():
                primary_objective = "Market Awareness"

            else:
                primary_objective = "Demand Generation"

        # -------------------------
        # SECONDARY OBJECTIVE
        # -------------------------

        if primary_objective == "Attention + Signal Building":
            secondary_objective = "Trust Formation"

        elif primary_objective == "Lead Generation":
            secondary_objective = "Authority Building"

        else:
            secondary_objective = "Conversion Efficiency"

        # -------------------------
        # KPI LOCKING
        # -------------------------

        if primary_objective == "Attention + Signal Building":
            kpi = "Reach + Saves + Profile Visits"

        elif primary_objective == "Lead Generation":
            kpi = "Qualified Leads"

        elif primary_objective == "Revenue Growth":
            kpi = "ROAS + Conversion Rate"

        else:
            kpi = "Engagement + CTR"

        # -------------------------
        # TIMELINE REALITY CHECK
        # -------------------------

        if lifecycle_stage == "Foundational":
            timeline = "90–120 days realistic"

        elif urgency_level == "High":
            timeline = "Expect phased growth (not instant)"

        else:
            timeline = "60–90 days realistic"

        # -------------------------
        # SCOPE CONTROL
        # -------------------------

        if monthly_budget < 40000:
            scope_control = "Narrow execution scope required"

        elif monthly_budget < 80000:
            scope_control = "Focused growth execution"

        else:
            scope_control = "Full-scale execution allowed"

        # -------------------------
        # COMMERCIAL MODE
        # -------------------------

        if lifecycle_stage == "Foundational":
            commercial_mode = "Foundation Build Mode"

        elif primary_objective == "Lead Generation":
            commercial_mode = "Acquisition Mode"

        else:
            commercial_mode = "Growth Mode"

        return {
            "primary_objective": primary_objective,
            "secondary_objective": secondary_objective,
            "locked_kpi": kpi,
            "timeline_expectation": timeline,
            "scope_control": scope_control,
            "commercial_mode": commercial_mode
        }