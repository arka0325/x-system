class LifecycleEngine:

    def evaluate(
        self,
        brand_stage,
        follower_count=None,
        post_count=None,
        website_age_days=None,
    ):
        if brand_stage == "Foundational":
            return {
                "lifecycle_stage": "Foundational",
                "confidence": "Manual Override",
                "reasoning": "Manual brand stage selected as Foundational.",
            }

        foundational_signals = []

        if follower_count is not None and follower_count < 500:
            foundational_signals.append("Follower count below 500")

        if post_count is not None and post_count < 10:
            foundational_signals.append("Post count below 10")

        if website_age_days is not None and website_age_days < 90:
            foundational_signals.append("Website age below 90 days")

        if foundational_signals:
            return {
                "lifecycle_stage": "Foundational",
                "confidence": "Auto Detected",
                "reasoning": "; ".join(foundational_signals),
            }

        return {
            "lifecycle_stage": "Active",
            "confidence": "Auto Detected",
            "reasoning": "No foundational thresholds triggered.",
        }
