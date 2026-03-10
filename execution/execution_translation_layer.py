class ExecutionTranslationLayer:

    def translate(self, diagnosis, strategy, planning, execution, optimization, demand_validation):
        immediate_actions = []
        content_actions = []
        budget_actions = []
        risk_alerts = []

        demand_status = demand_validation.get("demand_status", "Unclear")
        lifecycle_stage = (
            strategy.get("lifecycle_stage")
            or diagnosis.get("lifecycle_stage")
            or "Active"
        )
        primary_mode = diagnosis.get("primary_mode", "")
        risk_level = str(diagnosis.get("risk_level", "Low"))

        permutation = diagnosis.get("pillar_permutation", {})
        weakest_pillar = permutation.get("weakest_pillar", "")

        if demand_status == "Premature" or lifecycle_stage == "Foundational":
            immediate_actions.extend(
                [
                    "Focus only on positioning clarity and signal-building content.",
                    "Pause paid ads and allocate effort to organic authority-building.",
                    "Do not run scaling experiments until baseline demand signals appear.",
                ]
            )
            next_30_day_focus = "Focus on signal-building and positioning clarity for next 30 days."
            return {
                "immediate_actions": self._dedupe(immediate_actions),
                "content_actions": self._dedupe(content_actions),
                "budget_actions": [],
                "risk_alerts": self._dedupe(risk_alerts),
                "next_30_day_focus": next_30_day_focus,
            }

        if primary_mode == "Reposition":
            immediate_actions.extend(
                [
                    "Rewrite the core offer statement around one specific customer outcome.",
                    "Clarify the category position in one sentence your audience can repeat.",
                    "Strengthen differentiation by defining what your brand does differently.",
                ]
            )

        if primary_mode == "Optimize":
            immediate_actions.extend(
                [
                    "Double down on the top performing content type from the last 2-4 weeks.",
                    "Increase budget in channels where ROAS is consistently above target.",
                ]
            )

        if weakest_pillar == "Logic_with_Trust":
            content_actions.extend(
                [
                    "Add one testimonial-led post this week to increase trust signals.",
                    "Publish one proof breakdown reel showing process and measurable result.",
                ]
            )

        if weakest_pillar == "Lead_with_Value":
            content_actions.extend(
                [
                    "Rewrite CTA copy in outcome-driven language.",
                    "Add a benefit-first headline to your next offer post.",
                ]
            )

        if risk_level == "High":
            risk_alerts.extend(
                [
                    "Pause scaling activity until performance stabilizes.",
                    "Fix hook CTR before increasing spend.",
                ]
            )

        budget_actions.extend(self._translate_budget_allocation(strategy))
        budget_actions.extend(self._translate_scaling_thresholds(strategy))

        if demand_status == "Weak":
            next_30_day_focus = (
                "Run message-market fit tests and tighten problem-to-offer articulation."
            )
        elif demand_status == "Unclear":
            next_30_day_focus = (
                "Run structured audience validation and compare demand signals across content themes."
            )
        elif primary_mode == "Optimize":
            next_30_day_focus = (
                "Scale winning assets carefully while reinforcing the weakest strategic pillar."
            )
        else:
            next_30_day_focus = (
                "Execute focused growth sprints while monitoring demand and pillar balance weekly."
            )

        return {
            "immediate_actions": self._dedupe(immediate_actions),
            "content_actions": self._dedupe(content_actions),
            "budget_actions": self._dedupe(budget_actions),
            "risk_alerts": self._dedupe(risk_alerts),
            "next_30_day_focus": next_30_day_focus,
        }

    def _translate_budget_allocation(self, strategy):
        actions = []
        allocation = strategy.get("budget_allocation", {})
        total_budget = strategy.get("monthly_budget")

        if not isinstance(allocation, dict) or not allocation:
            return actions

        for channel, raw_value in allocation.items():
            percent = self._as_percent(raw_value)
            if percent is None:
                continue

            if isinstance(total_budget, (int, float)) and total_budget > 0:
                amount = (percent / 100.0) * float(total_budget)
                actions.append(
                    f"Allocate {percent:.0f}% of budget ({self._currency(amount)} of {self._currency(total_budget)} monthly) to {channel}."
                )
            else:
                actions.append(
                    f"Allocate {percent:.0f}% of your total ad budget to {channel} campaigns."
                )

        return actions

    def _translate_scaling_thresholds(self, strategy):
        actions = []
        thresholds = strategy.get("scaling_thresholds", {})

        if not isinstance(thresholds, dict) or not thresholds:
            return actions

        scale_up = thresholds.get("scale_up")
        if isinstance(scale_up, dict):
            roas = scale_up.get("roas")
            ctr = scale_up.get("ctr")
            if roas is not None and ctr is not None:
                actions.append(
                    f"If ROAS exceeds {roas} AND CTR exceeds {ctr}%, increase budget by 10-15%."
                )
                return actions

        min_roas = thresholds.get("min_roas_for_scale")
        min_ctr = thresholds.get("min_ctr_for_scale")
        min_conv = thresholds.get("min_conversion_rate")

        if min_roas is not None and min_ctr is not None:
            actions.append(
                f"If ROAS exceeds {min_roas} AND CTR exceeds {min_ctr}%, increase budget by 10-15%."
            )
        elif min_roas is not None and min_conv is not None:
            actions.append(
                f"If ROAS exceeds {min_roas} and conversion rate stays above {min_conv}%, increase budget by 10-15%."
            )

        return actions

    def _as_percent(self, value):
        if not isinstance(value, (int, float)):
            return None
        if value <= 1:
            return float(value) * 100.0
        return float(value)

    def _currency(self, value):
        return f"₹{float(value):,.0f}"

    def _dedupe(self, items):
        deduped = []
        seen = set()
        for item in items:
            if item not in seen:
                deduped.append(item)
                seen.add(item)
        return deduped
