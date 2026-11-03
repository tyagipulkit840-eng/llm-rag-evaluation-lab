package com.pulkit.llmeval.controller;

import com.pulkit.llmeval.model.EvaluationRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClient;

import java.util.Map;

@RestController
@RequestMapping("/api/evaluations")
public class EvaluationController {
    private final RestClient restClient;
    private final String evaluatorUrl;

    public EvaluationController(
            RestClient.Builder builder,
            @Value("${evaluator.base-url:http://localhost:8000}") String evaluatorUrl) {
        this.restClient = builder.build();
        this.evaluatorUrl = evaluatorUrl;
    }

    @PostMapping
    public Map evaluate(@RequestBody EvaluationRequest request) {
        Map result = restClient.post()
                .uri(evaluatorUrl + "/evaluate")
                .contentType(MediaType.APPLICATION_JSON)
                .body(Map.of(
                        "question", request.question(),
                        "reference_answer", request.referenceAnswer(),
                        "generated_answer", request.generatedAnswer(),
                        "retrieved_contexts", request.retrievedContexts() == null
                                ? java.util.List.of() : request.retrievedContexts()
                ))
                .retrieve()
                .body(Map.class);
        return result == null ? Map.of() : result;
    }

    @GetMapping("/health")
    public Map health() {
        return Map.of("status", "ok", "service", "java-api");
    }
}
