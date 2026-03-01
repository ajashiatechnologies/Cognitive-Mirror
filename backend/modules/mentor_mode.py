import json
from llm_engine import call_llm
from reasoning_engine import extract_json


def mentor_feedback(problem, structured_steps):

    prompt = f"""
You are an AI reasoning mentor.

Provide improvement suggestions for:

Problem:
{problem}

Steps:
{structured_steps}

Return STRICT JSON:

{{
  "strengths": ["string"],
  "improvement_areas": ["string"],
  "action_plan": ["string"]
}}

No explanation outside JSON.
"""

    response = call_llm(prompt)
    return json.loads(extract_json(response))