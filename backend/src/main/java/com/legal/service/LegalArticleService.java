package com.legal.service;

import com.legal.entity.LegalArticle;
import com.legal.repository.LegalArticleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class LegalArticleService {
    
    @Autowired
    private LegalArticleRepository legalArticleRepository;
    
    public Page<LegalArticle> searchArticles(String keyword, Pageable pageable) {
        return legalArticleRepository.findByTitleContainingOrContentContaining(keyword, keyword, pageable);
    }
    
    public List<LegalArticle> getArticlesByLawType(String lawType) {
        return legalArticleRepository.findByLawType(lawType);
    }
    
    public List<LegalArticle> getAllValidArticles() {
        return legalArticleRepository.findByIsValidTrue();
    }
    
    public Optional<LegalArticle> getArticleById(Long id) {
        return legalArticleRepository.findById(id);
    }
    
    @Transactional
    public LegalArticle saveArticle(LegalArticle article) {
        return legalArticleRepository.save(article);
    }
    
    @Transactional
    public void deleteArticle(Long id) {
        legalArticleRepository.deleteById(id);
    }
}

