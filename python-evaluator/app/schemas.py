from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    question: str = Field(min_length=1)
    reference_answer: str = Field(min_length=1)
    generated_answer: str = Field(min_length=1)
    retrieved_contexts: list[str] = Field(default_factory=list)


class EvaluationResponse(BaseModel):
    exact_match: float
    answer_token_coverage: float
    context_token_support: float
    overall_baseline_score: float
    passed: bool
    notes: list[str]
