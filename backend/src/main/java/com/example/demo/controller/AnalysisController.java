package com.example.demo.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

import com.example.demo.dto.AnalysisRequest;

@RestController
public class AnalysisController {

    private final WebClient pythonWebClient;

    public AnalysisController(WebClient pythonWebClient) {
        this.pythonWebClient = pythonWebClient;
    }

    @PostMapping("/api/analyses")
    public Map analyze(@RequestBody AnalysisRequest request) {

        String endpoint = "/internal/stats/" + request.getMethod();

        return pythonWebClient.post()
                .uri(endpoint)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(Map.class)
                .block();
    }
}
