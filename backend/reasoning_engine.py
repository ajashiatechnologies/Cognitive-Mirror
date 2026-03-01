import json
import re
from models import StepInput
from llm_engine import call_llm


def analyze_reasoning(data: StepInput):

    structured_steps = "\n".join(
        [f"Step {i+1}: {step}" for i, step in enumerate(data.steps)]
    )

    prompt = f"""
You are an advanced cognitive reasoning analyzer.

Analyze the following problem-solving steps.

Problem:
{data.problem_statement}

Steps:
{structured_steps}

Return STRICT JSON only with EXACTLY this structure:

{{
  "logical_gaps": [
      {{
        "step_number": int,
        "issue": "string"
      }}
  ],
  "assumptions_detected": ["string"],
  "contradictions": ["string"],
  "step_completeness_score": int,
  "logical_consistency_score": int,
  "reasoning_summary": "string"
}}

Rules:
- No text outside JSON.
- No explanations outside JSON.
- Always include all keys.
- Scores must be between 0 and 100.
"""

    llm_response = call_llm(prompt)

    json_text = extract_json(llm_response)

    try:
        parsed = json.loads(json_text)
    except Exception:
        raise Exception("LLM did not return valid JSON.")

    # ---- CORE QUALITY SCORE ----
    completeness = clamp(parsed.get("step_completeness_score", 0))
    consistency = clamp(parsed.get("logical_consistency_score", 0))

    quality_score = (completeness + consistency) // 2

    # ---- CONFIDENCE CALIBRATION ----
    confidence_alignment = evaluate_confidence(
        data.confidence_level,
        quality_score
    )

    # ---- ADVANCED SYNTHETIC COGNITIVE METRICS ----

    # Analytical Depth: weighted toward consistency
    analytical_depth = clamp(int((consistency * 0.6 + completeness * 0.4)))

    # Structural Coherence: strong consistency but penalize contradictions
    contradiction_penalty = len(parsed.get("contradictions", [])) * 5
    structural_coherence = clamp(consistency - contradiction_penalty)

    # Error Sensitivity: ability to detect reasoning gaps
    gap_count = len(parsed.get("logical_gaps", []))
    error_sensitivity = clamp(min(100, gap_count * 15))

    # Cognitive Risk Index: mismatch between confidence and quality
    confidence_scaled = data.confidence_level * 20
    cognitive_risk_index = clamp(abs(confidence_scaled - quality_score))

    # Cognitive Stability Index (composite metric)
    cognitive_stability_index = clamp(
        int((analytical_depth + structural_coherence) / 2 - cognitive_risk_index * 0.3)
    )

    # ---- REASONING GRAPH ----
    reasoning_graph = []
    for i in range(len(data.steps)):
        node = {
            "step_number": i + 1,
            "content": data.steps[i]
        }
        reasoning_graph.append(node)

    # ---- FINAL RESPONSE STRUCTURE ----
    parsed.update({
        "overall_cognitive_score": quality_score,
        "confidence_alignment": confidence_alignment,
        "analytical_depth": analytical_depth,
        "structural_coherence": structural_coherence,
        "error_sensitivity": error_sensitivity,
        "cognitive_risk_index": cognitive_risk_index,
        "cognitive_stability_index": cognitive_stability_index,
        "reasoning_graph": reasoning_graph
    })

    return parsed

def multi_agent_analysis(data: StepInput):

    structured_steps = "\n".join(
        [f"Step {i+1}: {step}" for i, step in enumerate(data.steps)]
    )

    logical_prompt = f"""
You are a STRICT LOGICAL ANALYZER.
Focus only on mathematical correctness, structure and contradictions.

Problem:
{data.problem_statement}

Steps:
{structured_steps}

Return JSON:
{{
  "logical_strength": int,
  "structural_integrity": int,
  "error_density": int,
  "summary": "string"
}}
Scores 0-100 only.
"""

    creative_prompt = f"""
You are a CREATIVE REASONING ANALYZER.
Focus on flexibility, insight depth and conceptual abstraction.

Problem:
{data.problem_statement}

Steps:
{structured_steps}

Return JSON:
{{
  "creative_depth": int,
  "conceptual_flexibility": int,
  "innovation_score": int,
  "summary": "string"
}}
Scores 0-100 only.
"""

    logical_response = call_llm(logical_prompt)
    creative_response = call_llm(creative_prompt)

    logical = json.loads(extract_json(logical_response))
    creative = json.loads(extract_json(creative_response))

    return {
        "logical_agent": logical,
        "creative_agent": creative
    }
# -------------------------------
# UTILITIES
# -------------------------------

def extract_json(text: str):
    """
    Extract JSON block safely from LLM output.
    Handles cases where model adds extra commentary.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def evaluate_confidence(confidence_level, quality_score):

    confidence_scaled = confidence_level * 20
    difference = confidence_scaled - quality_score

    if difference > 20:
        return "Strongly Overconfident"
    elif difference > 10:
        return "Slightly Overconfident"
    elif difference < -20:
        return "Strongly Underconfident"
    elif difference < -10:
        return "Slightly Underconfident"
    else:
        return "Well-Calibrated"


def clamp(value, min_val=0, max_val=100):
    """
    Ensures all cognitive metrics stay between 0 and 100.
    """
    return max(min_val, min(max_val, int(value)))