package com.legal.service;

import com.legal.entity.KnowledgeBase;
import com.legal.repository.KnowledgeBaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class KnowledgeBaseService {
    
    @Autowired
    private KnowledgeBaseRepository knowledgeBaseRepository;
    
    public Page<KnowledgeBase> searchKnowledge(String keyword, Pageable pageable) {
        return knowledgeBaseRepository.findByQuestionContainingOrAnswerContaining(keyword, keyword, pageable);
    }
    
    public List<KnowledgeBase> getKnowledgeByType(String questionType) {
        return knowledgeBaseRepository.findByQuestionType(questionType);
    }
    
    public List<KnowledgeBase> getKnowledgeByLawType(String lawType) {
        return knowledgeBaseRepository.findByLawType(lawType);
    }
    
    public Optional<KnowledgeBase> getKnowledgeById(Long id) {
        return knowledgeBaseRepository.findById(id);
    }
    
    @Transactional
    public KnowledgeBase saveKnowledge(KnowledgeBase knowledge) {
        return knowledgeBaseRepository.save(knowledge);
    }
    
    @Transactional
    public void deleteKnowledge(Long id) {
        knowledgeBaseRepository.deleteById(id);
    }
    
    @Transactional
    public void incrementUsageCount(Long id) {
        Optional<KnowledgeBase> knowledge = knowledgeBaseRepository.findById(id);
        if (knowledge.isPresent()) {
            KnowledgeBase kb = knowledge.get();
            kb.setUsageCount(kb.getUsageCount() + 1);
            knowledgeBaseRepository.save(kb);
        }
    }
}

