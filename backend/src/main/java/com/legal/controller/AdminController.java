package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.entity.*;
import com.legal.repository.QuestionAnswerRepository;
import com.legal.service.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/admin")
@CrossOrigin
public class AdminController {
    
    @Autowired
    private KnowledgeBaseService knowledgeBaseService;
    
    @Autowired
    private LegalArticleService legalArticleService;
    
    @Autowired
    private LegalCaseService legalCaseService;
    
    @Autowired
    private LegalConceptService legalConceptService;
    
    @Autowired
    private QuestionAnswerRepository questionAnswerRepository;
    
    // 知识库管理
    @GetMapping("/knowledge")
    public ApiResponse<Page<KnowledgeBase>> getKnowledge(
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Pageable pageable = PageRequest.of(page, size);
        if (keyword != null && !keyword.isEmpty()) {
            return ApiResponse.success(knowledgeBaseService.searchKnowledge(keyword, pageable));
        }
        return ApiResponse.success(knowledgeBaseService.searchKnowledge("", pageable));
    }
    
    @PostMapping("/knowledge")
    public ApiResponse<KnowledgeBase> createKnowledge(@RequestBody KnowledgeBase knowledge) {
        return ApiResponse.success(knowledgeBaseService.saveKnowledge(knowledge));
    }
    
    @PutMapping("/knowledge/{id}")
    public ApiResponse<KnowledgeBase> updateKnowledge(@PathVariable Long id, @RequestBody KnowledgeBase knowledge) {
        knowledge.setId(id);
        return ApiResponse.success(knowledgeBaseService.saveKnowledge(knowledge));
    }
    
    @DeleteMapping("/knowledge/{id}")
    public ApiResponse<?> deleteKnowledge(@PathVariable Long id) {
        knowledgeBaseService.deleteKnowledge(id);
        return ApiResponse.success("删除成功");
    }
    
    // 法条管理
    @PostMapping("/article")
    public ApiResponse<LegalArticle> createArticle(@RequestBody LegalArticle article) {
        return ApiResponse.success(legalArticleService.saveArticle(article));
    }
    
    @PutMapping("/article/{id}")
    public ApiResponse<LegalArticle> updateArticle(@PathVariable Long id, @RequestBody LegalArticle article) {
        article.setId(id);
        return ApiResponse.success(legalArticleService.saveArticle(article));
    }
    
    @DeleteMapping("/article/{id}")
    public ApiResponse<?> deleteArticle(@PathVariable Long id) {
        legalArticleService.deleteArticle(id);
        return ApiResponse.success("删除成功");
    }
    
    // 案例管理
    @PostMapping("/case")
    public ApiResponse<LegalCase> createCase(@RequestBody LegalCase legalCase) {
        return ApiResponse.success(legalCaseService.saveCase(legalCase));
    }
    
    @PutMapping("/case/{id}")
    public ApiResponse<LegalCase> updateCase(@PathVariable Long id, @RequestBody LegalCase legalCase) {
        legalCase.setId(id);
        return ApiResponse.success(legalCaseService.saveCase(legalCase));
    }
    
    @DeleteMapping("/case/{id}")
    public ApiResponse<?> deleteCase(@PathVariable Long id) {
        legalCaseService.deleteCase(id);
        return ApiResponse.success("删除成功");
    }
    
    // 概念管理
    @PostMapping("/concept")
    public ApiResponse<LegalConcept> createConcept(@RequestBody LegalConcept concept) {
        return ApiResponse.success(legalConceptService.saveConcept(concept));
    }
    
    @PutMapping("/concept/{id}")
    public ApiResponse<LegalConcept> updateConcept(@PathVariable Long id, @RequestBody LegalConcept concept) {
        concept.setId(id);
        return ApiResponse.success(legalConceptService.saveConcept(concept));
    }
    
    @DeleteMapping("/concept/{id}")
    public ApiResponse<?> deleteConcept(@PathVariable Long id) {
        legalConceptService.deleteConcept(id);
        return ApiResponse.success("删除成功");
    }
    
    // 统计数据
    @GetMapping("/stats")
    public ApiResponse<Map<String, Object>> getStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("todayQuestions", questionAnswerRepository.countTodayQuestions());
        stats.put("questionTypes", questionAnswerRepository.countByQuestionType());
        return ApiResponse.success(stats);
    }
    
    // 问答记录管理
    @GetMapping("/qa")
    public ApiResponse<Page<QuestionAnswer>> getQARecords(
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {
        Pageable pageable = PageRequest.of(page, size);
        if (keyword != null && !keyword.isEmpty()) {
            return ApiResponse.success(questionAnswerRepository.findByQuestionContaining(keyword, pageable));
        }
        return ApiResponse.success(questionAnswerRepository.findAll(pageable));
    }
}

