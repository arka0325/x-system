class BrandDemandModel:

    def calculate(self, BS, C, T, demand_status="Validated"):
        if demand_status != "Validated":
            return {
                "Brand_Strength": BS,
                "Demand_Validation": demand_status,
                "Brand_Demand_Score": None,
                "Interpretation": "Demand not validated yet."
            }

        GF = (C / 30) * (T / 12)
        BD = BS * (C / 30) * (T / 12)

        interpretation = self._interpret(BD)

        return {
            "Brand_Strength": BS,
            "Growth_Factor": round(GF, 2),
            "Brand_Demand_Score": round(BD, 2),
            "Interpretation": interpretation
        }

    def _interpret(self, BD):

        if BD <= 5:
            return "Invisible Phase"
        elif BD <= 15:
            return "Early Traction"
        elif BD <= 30:
            return "Strong Positioning"
        elif BD <= 60:
            return "Category Authority"
        else:
            return "Dominant Positioning"
