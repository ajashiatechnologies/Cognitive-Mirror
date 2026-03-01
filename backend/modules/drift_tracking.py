def reasoning_drift_analysis(steps):

    drift_score = 0

    for i in range(1, len(steps)):
        prev = steps[i - 1].lower()
        curr = steps[i].lower()

        if prev not in curr and len(curr) > len(prev) * 1.5:
            drift_score += 10

    drift_score = min(drift_score, 100)

    return {
        "drift_score": drift_score,
        "interpretation":
            "High reasoning shift detected"
            if drift_score > 50 else
            "Stable reasoning progression"
    }