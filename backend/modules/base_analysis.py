import json
from llm_engine import call_llm
from reasoning_engine import extract_json


def logical_analysis(problem, structured_steps):

    prompt = f"""
You are a strict logical reasoning evaluator.

Evaluate:
- Logical correctness
- Structural clarity
- Error density
- Step dependency integrity

Problem:
{problem}

Steps:
{structured_steps}

Return STRICT JSON:

{{
  "logical_strength": int,
  "structural_integrity": int,
  "error_density": int,
  "analytical_depth": int,
  "summary": "string"
}}

Scores between 0-100 only.
No explanation outside JSON.
"""

    response = call_llm(prompt)
    return json.loads(extract_json(response))


def creative_analysis(problem, structured_steps):

    prompt = f"""
You are a creative reasoning evaluator.

Evaluate:
- Conceptual flexibility
- Innovation
- Abstract reasoning
- Alternative solution depth

Problem:
{problem}

Steps:
{structured_steps}

Return STRICT JSON:

{{
  "creative_depth": int,
  "conceptual_flexibility": int,
  "innovation_score": int,
  "divergent_thinking": int,
  "summary": "string"
}}

Scores between 0-100 only.
No explanation outside JSON.
"""

    response = call_llm(prompt)
    return json.loads(extract_json(response))