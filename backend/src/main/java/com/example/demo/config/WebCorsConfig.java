package com.example.demo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebCorsConfig implements WebMvcConfigurer {

	@Override
	public void addCorsMappings(CorsRegistry registry) {
		registry.addMapping("/**")
				.allowedOriginPatterns("http://localhost:5173",
						"https://frontend.victorioussmoke-9874bef0.japaneast.azurecontainerapps.io")
				.allowedMethods("*").allowedHeaders("*").allowCredentials(true);
	}
}
