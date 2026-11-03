import re
from .schemas import EvaluationRequest, EvaluationResponse


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    reference_tokens = _tokens(request.reference_answer)
    answer_tokens = _tokens(request.generated_answer)
    context_tokens = _tokens(" ".join(request.retrieved_contexts))

    exact_match = float(
        " ".join(request.reference_answer.lower().split())
        == " ".join(request.generated_answer.lower().split())
    )
    answer_coverage = (
        len(reference_tokens & answer_tokens) / len(reference_tokens)
        if reference_tokens else 0.0
    )
    context_support = (
        len(answer_tokens & context_tokens) / len(answer_tokens)
        if answer_tokens and context_tokens else 0.0
    )

    # A simple, explainable baseline. This is not a semantic or RAGAS score.
    overall = round((answer_coverage * 0.5) + (context_support * 0.5), 4)
    passed = answer_coverage >= 0.5 and context_support >= 0.5

    notes = [
        "Heuristic token-overlap baseline; not a semantic LLM judge.",
        "Use RAGAS or human review for deeper faithfulness and relevancy evaluation.",
    ]
    if not request.retrieved_contexts:
        notes.append("No retrieved contexts supplied; context support is 0.")

    return EvaluationResponse(
        exact_match=round(exact_match, 4),
        answer_token_coverage=round(answer_coverage, 4),
        context_token_support=round(context_support, 4),
        overall_baseline_score=overall,
        passed=passed,
        notes=notes,
    )
