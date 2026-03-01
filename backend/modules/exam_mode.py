def exam_simulation(logical, bias):

    exam_readiness_score = (
        logical["logical_strength"] * 0.6 +
        (100 - bias["cognitive_risk_index"]) * 0.4
    )

    performance_band = (
        "Elite"
        if exam_readiness_score > 85 else
        "Advanced"
        if exam_readiness_score > 70 else
        "Moderate"
        if exam_readiness_score > 50 else
        "Needs Improvement"
    )

    return {
        "exam_readiness_score": exam_readiness_score,
        "performance_band": performance_band
    }