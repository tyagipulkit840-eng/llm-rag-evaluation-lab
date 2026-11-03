from fastapi.testclient import TestClient
from app.main import app
from app.evaluator import evaluate
from app.schemas import EvaluationRequest

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_evaluation_returns_expected_fields():
    payload = {
        "question": "What is RAG?",
        "reference_answer": "RAG retrieves relevant external information and uses it to generate a grounded answer.",
        "generated_answer": "RAG retrieves external information and uses it to produce a grounded response.",
        "retrieved_contexts": [
            "Retrieval-Augmented Generation retrieves relevant information and supplies it to a language model."
        ],
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["overall_baseline_score"] <= 1
    assert "passed" in body
    assert "context_token_support" in body


def test_no_context_means_zero_context_support():
    request = EvaluationRequest(
        question="What is RAG?",
        reference_answer="RAG retrieves information.",
        generated_answer="RAG retrieves information.",
        retrieved_contexts=[],
    )
    result = evaluate(request)
    assert result.context_token_support == 0
    assert result.passed is False
