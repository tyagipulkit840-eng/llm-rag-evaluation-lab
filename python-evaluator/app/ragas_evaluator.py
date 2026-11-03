"""Optional RAGAS integration starter.

RAGAS APIs evolve. This file is intentionally isolated from the default API so
the baseline service and tests work without provider credentials. Consult the
current RAGAS docs before enabling/updating this adapter.
"""

async def evaluate_with_ragas(
    question: str,
    answer: str,
    retrieved_contexts: list[str],
):
    try:
        from openai import AsyncOpenAI
        from ragas.llms import llm_factory
        from ragas.metrics.collections import Faithfulness
    except ImportError as exc:
        raise RuntimeError(
            "Install optional dependencies: pip install -r requirements-ragas.txt"
        ) from exc

    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY before running RAGAS evaluation.")

    client = AsyncOpenAI(api_key=api_key)
    judge_llm = llm_factory("gpt-4o-mini", client=client)
    faithfulness = Faithfulness(llm=judge_llm)
    result = await faithfulness.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=retrieved_contexts,
    )
    return {"faithfulness": float(result.value)}
