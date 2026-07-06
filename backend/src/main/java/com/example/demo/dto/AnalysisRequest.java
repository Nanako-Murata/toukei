package com.example.demo.dto;

import java.util.List;
import java.util.Map;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AnalysisRequest {
	private List<GroupData> groups;
	private String method;
	private Map<String, Object> options;

}
