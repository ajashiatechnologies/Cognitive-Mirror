def compute_ensemble(logical, creative, bias, drift):

    logical_avg = (
        logical["logical_strength"] +
        logical["structural_integrity"]
    ) / 2

    creative_avg = (
        creative["creative_depth"] +
        creative["conceptual_flexibility"]
    ) / 2

    cognitive_intelligence_index = (
        logical_avg * 0.35 +
        creative_avg * 0.25 +
        bias["meta_cognition_score"] * 0.25 +
        (100 - bias["cognitive_risk_index"]) * 0.15
    )

    disagreement_index = abs(logical_avg - creative_avg)

    return {
        "logical_average": logical_avg,
        "creative_average": creative_avg,
        "disagreement_index": disagreement_index,
        "cognitive_intelligence_index": cognitive_intelligence_index,
        "drift_score": drift["drift_score"]
    }