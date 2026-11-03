package com.pulkit.llmeval.model;

import java.util.List;

public record EvaluationRequest(
        String question,
        String referenceAnswer,
        String generatedAnswer,
        List<String> retrievedContexts
) {}
