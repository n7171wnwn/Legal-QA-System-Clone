package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.entity.LegalArticle;
import com.legal.service.LegalArticleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/legal/article")
@CrossOrigin
public class LegalArticleController {
    
    @Autowired
    private LegalArticleService legalArticleService;
    
    @GetMapping("/search")
    public ApiResponse<Page<LegalArticle>> searchArticles(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Pageable pageable = PageRequest.of(page, size);
        return ApiResponse.success(legalArticleService.searchArticles(keyword, pageable));
    }
    
    @GetMapping("/type/{lawType}")
    public ApiResponse<List<LegalArticle>> getArticlesByType(@PathVariable String lawType) {
        return ApiResponse.success(legalArticleService.getArticlesByLawType(lawType));
    }
    
    @GetMapping("/{id}")
    public ApiResponse<LegalArticle> getArticle(@PathVariable Long id) {
        return legalArticleService.getArticleById(id)
                .map(ApiResponse::success)
                .orElse(ApiResponse.error("法条不存在"));
    }
    
    @GetMapping("/all")
    public ApiResponse<List<LegalArticle>> getAllArticles() {
        return ApiResponse.success(legalArticleService.getAllValidArticles());
    }
}

