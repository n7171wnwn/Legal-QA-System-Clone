package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.entity.LegalCase;
import com.legal.service.LegalCaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/legal/case")
@CrossOrigin
public class LegalCaseController {
    
    @Autowired
    private LegalCaseService legalCaseService;
    
    @GetMapping("/search")
    public ApiResponse<Page<LegalCase>> searchCases(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Pageable pageable = PageRequest.of(page, size);
        return ApiResponse.success(legalCaseService.searchCases(keyword, pageable));
    }
    
    @GetMapping("/type/{lawType}")
    public ApiResponse<List<LegalCase>> getCasesByType(@PathVariable String lawType) {
        return ApiResponse.success(legalCaseService.getCasesByLawType(lawType));
    }
    
    @GetMapping("/{id}")
    public ApiResponse<LegalCase> getCase(@PathVariable Long id) {
        return legalCaseService.getCaseById(id)
                .map(ApiResponse::success)
                .orElse(ApiResponse.error("案例不存在"));
    }
}

