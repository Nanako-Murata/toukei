package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
public class PingTestController {
	private final WebClient pythonWebClient;

	public PingTestController(WebClient pythonWebClient) {
		this.pythonWebClient = pythonWebClient;
	}

	@GetMapping("/test-ping")
	public String testPing() {
		return pythonWebClient.get().uri("/ping").retrieve().bodyToMono(String.class).block();
	}

}
