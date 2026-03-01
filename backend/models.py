from pydantic import BaseModel
from typing import List

class StepInput(BaseModel):
    problem_statement: str
    steps: List[str]
    confidence_level: int  # 1 to 5

class CognitiveResponse(BaseModel):
    logical_gaps: List[str]
    assumptions_detected: List[str]
    contradictions: List[str]
    step_completeness_score: int
    logical_consistency_score: int
    reasoning_summary: str
    confidence_alignment: str
    overall_cognitive_score: int