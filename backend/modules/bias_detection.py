import json
from llm_engine import call_llm
from reasoning_engine import extract_json


def bias_analysis(problem, structured_steps, confidence_level):

    prompt = f"""
You are a cognitive bias detection system.

Analyze reasoning for:
- Confirmation bias
- Overconfidence bias
- Emotional reasoning
- Anchoring bias
- Logical shortcuts
- Cascading error probability

Confidence level given by user: {confidence_level} (1-5 scale)

Problem:
{problem}

Steps:
{structured_steps}

Return STRICT JSON:

{{
  "confirmation_bias_risk": int,
  "overconfidence_risk": int,
  "emotional_reasoning_score": int,
  "anchoring_bias_risk": int,
  "cognitive_risk_index": int,
  "meta_cognition_score": int,
  "summary": "string"
}}

Scores between 0-100 only.
No explanation outside JSON.
"""

    response = call_llm(prompt)
    return json.loads(extract_json(response))