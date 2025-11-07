package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.entity.LegalConcept;
import com.legal.service.LegalConceptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/legal/concept")
@CrossOrigin
public class LegalConceptController {
    
    @Autowired
    private LegalConceptService legalConceptService;
    
    @GetMapping("/search")
    public ApiResponse<Page<LegalConcept>> searchConcepts(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Pageable pageable = PageRequest.of(page, size);
        return ApiResponse.success(legalConceptService.searchConcepts(keyword, pageable));
    }
    
    @GetMapping("/name/{name}")
    public ApiResponse<LegalConcept> getConceptByName(@PathVariable String name) {
        return legalConceptService.getConceptByName(name)
                .map(ApiResponse::success)
                .orElse(ApiResponse.error("概念不存在"));
    }
    
    @GetMapping("/{id}")
    public ApiResponse<LegalConcept> getConcept(@PathVariable Long id) {
        return legalConceptService.getConceptById(id)
                .map(ApiResponse::success)
                .orElse(ApiResponse.error("概念不存在"));
    }
}

