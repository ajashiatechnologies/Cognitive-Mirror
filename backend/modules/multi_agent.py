from models import StepInput
from modules.base_analysis import logical_analysis, creative_analysis
from modules.bias_detection import bias_analysis
from modules.drift_tracking import reasoning_drift_analysis
from modules.ensemble import compute_ensemble
from modules.exam_mode import exam_simulation
from modules.mentor_mode import mentor_feedback


def multi_agent_analysis(data: StepInput):

    structured_steps = "\n".join(
        [f"Step {i+1}: {step}" for i, step in enumerate(data.steps)]
    )

    # ---------------- CORE AGENTS ----------------

    logical = logical_analysis(
        data.problem_statement,
        structured_steps
    )

    creative = creative_analysis(
        data.problem_statement,
        structured_steps
    )

    bias = bias_analysis(
        data.problem_statement,
        structured_steps,
        data.confidence_level
    )

    drift = reasoning_drift_analysis(data.steps)

    # ---------------- ENSEMBLE ----------------

    ensemble = compute_ensemble(
        logical,
        creative,
        bias,
        drift
    )

    # ---------------- EXAM MODE ----------------

    exam = exam_simulation(logical, bias)

    # ---------------- MENTOR MODE ----------------

    mentor = mentor_feedback(
        data.problem_statement,
        structured_steps
    )

    return {
        "logical_agent": logical,
        "creative_agent": creative,
        "bias_agent": bias,
        "drift_analysis": drift,
        "ensemble": ensemble,
        "exam_mode": exam,
        "mentor_mode": mentor
    }