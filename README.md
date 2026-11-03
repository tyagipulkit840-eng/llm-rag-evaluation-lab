# LLM RAG Evaluation Lab

A portfolio starter project for evaluating Retrieval-Augmented Generation (RAG) outputs with a QA-engineering mindset.

**Stack:** Python · FastAPI · Pytest · RAGAS (optional adapter) · Java 17 · Spring Boot · Maven · Docker Compose

## What this project demonstrates

- A versioned evaluation dataset with questions, reference answers, generated answers, and retrieved contexts.
- Deterministic baseline checks for exact match, answer coverage, and context support.
- A Python FastAPI evaluation service.
- A Java Spring Boot API that forwards evaluation requests to the Python service.
- Unit and API tests with Pytest and JUnit.
- An optional RAGAS integration for LLM-based metrics such as faithfulness and answer relevancy.
- Docker Compose for running both services together.

> This repository is a learning/portfolio starter. The baseline metrics are transparent heuristics, not substitutes for semantic LLM evaluation. The optional RAGAS adapter requires an LLM provider API key. Do not describe the optional RAGAS path as executed until you configure and run it.

## Architecture

```text
Client
  |
  v
Java Spring Boot API :8080
  |
  | HTTP POST /evaluate
  v
Python FastAPI evaluator :8000
  |
  +-- deterministic QA checks (no API key)
  |
  +-- optional RAGAS LLM evaluation (API key required)
```

## Repository layout

```text
llm-rag-evaluation-lab/
├── python-evaluator/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── evaluator.py
│   ├── data/sample_dataset.json
│   ├── tests/test_evaluator.py
│   ├── requirements.txt
│   └── requirements-ragas.txt
├── java-api/
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/pulkit/llmeval/...
│       └── test/java/com/pulkit/llmeval/...
├── .github/workflows/tests.yml
├── docker-compose.yml
└── .gitignore
```

## Run the Python evaluator

Requires Python 3.10+.

```bash
cd python-evaluator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open the interactive API docs at `http://localhost:8000/docs`.

Example request:

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "reference_answer": "RAG retrieves relevant external information and uses it to generate a grounded answer.",
    "generated_answer": "RAG retrieves external information and uses it to produce a grounded response.",
    "retrieved_contexts": [
      "Retrieval-Augmented Generation retrieves relevant information and supplies it to a language model."
    ]
  }'
```

## Run the Java API

In another terminal, from the repository root:

```bash
cd java-api
mvn spring-boot:run
```

The Java API listens on `http://localhost:8080` and forwards evaluation requests to Python at `http://localhost:8000`.

Example:

```bash
curl -X POST http://localhost:8080/api/evaluations \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "referenceAnswer": "RAG retrieves relevant external information and uses it to generate a grounded answer.",
    "generatedAnswer": "RAG retrieves external information and uses it to produce a grounded response.",
    "retrievedContexts": [
      "Retrieval-Augmented Generation retrieves relevant information and supplies it to a language model."
    ]
  }'
```

Start the Python service before calling the Java endpoint.

## Run tests

Python:

```bash
cd python-evaluator
pip install -r requirements.txt
pytest -q
```

Java:

```bash
cd java-api
mvn test
```

## Run both services with Docker Compose

From the repository root:

```bash
docker compose up --build
```

- Java API: `http://localhost:8080`
- Python evaluator: `http://localhost:8000`
- Python API docs: `http://localhost:8000/docs`

## Optional: configure RAGAS

The default baseline is API-key-free. To explore model-judged evaluation, install the optional dependencies:

```bash
cd python-evaluator
pip install -r requirements-ragas.txt
```

Set an OpenAI-compatible key in your shell:

```bash
export OPENAI_API_KEY="your-api-key"
```

Then use the RAGAS adapter in `app/ragas_evaluator.py` as a starting point. LLM-based metrics make external model calls and may incur provider costs. Review current RAGAS documentation before upgrading dependencies because its metric APIs evolve.

Useful metric concepts:
- **Faithfulness:** whether answer claims are supported by retrieved context.
- **Answer relevancy:** whether the answer addresses the user's question.
- **Context precision:** whether retrieved chunks are relevant and well-ranked.

## Suggested next improvements

1. Add a document ingestion and chunking pipeline.
2. Add a vector store such as FAISS or Chroma.
3. Connect a real LLM for answer generation.
4. Add RAGAS evaluation to the CI workflow using secured repository secrets.
5. Store evaluation runs and compare scores across model/prompt versions.
6. Add HTML reports and regression thresholds.

## Author

**Pulkit Tyagi**  
Software Engineer | LLM Applications | AI Evaluation | QA Automation  
Roorkee, India · [LinkedIn](https://linkedin.com/in/pulkit-tyagi14)

This project is intended to demonstrate ongoing learning. Only claim features you have configured, run, and can explain.
