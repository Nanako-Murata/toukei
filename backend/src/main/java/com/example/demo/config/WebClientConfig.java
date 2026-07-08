package com.example.demo.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {
	
	 @Value("${python.service.url:http://127.0.0.1:8000}")
	    private String pythonServiceUrl;

	
	@Bean
	public WebClient pythonWebClient() {
		return WebClient.builder()
				.baseUrl(pythonServiceUrl)
				.build();
	}

}
