from fastapi import FastAPI
from .schemas import EvaluationRequest, EvaluationResponse
from .evaluator import evaluate

app = FastAPI(
    title="LLM RAG Evaluation API",
    description="QA-oriented baseline evaluation for RAG responses.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "python-evaluator"}


@app.post("/evaluate", response_model=EvaluationResponse)
def run_evaluation(request: EvaluationRequest):
    return evaluate(request)
