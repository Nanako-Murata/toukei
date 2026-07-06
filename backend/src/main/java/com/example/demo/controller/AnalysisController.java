package com.example.demo.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

import com.example.demo.dto.AnalysisRequest;

@RestController
@CrossOrigin(origins = "http://localhost:5173")
public class AnalysisController {
	private final WebClient pythonWebClient;
	public AnalysisController(WebClient pythonWebClient) {
		this.pythonWebClient = pythonWebClient;
	}
	  @PostMapping("/api/analyses")
	    public Map analyze(@RequestBody AnalysisRequest request) {
	        // 現時点ではbasicのみ対応。method名からPython側のエンドポイントへ振り分け
	        String endpoint = "/internal/stats/" + request.getMethod();

	        return pythonWebClient.post()
	                .uri(endpoint)
	                .bodyValue(request)
	                .retrieve()
	                .bodyToMono(Map.class)
	                .block();
	    }

}
