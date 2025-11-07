package com.legal.service;

import com.legal.entity.LegalCase;
import com.legal.repository.LegalCaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class LegalCaseService {
    
    @Autowired
    private LegalCaseRepository legalCaseRepository;
    
    public Page<LegalCase> searchCases(String keyword, Pageable pageable) {
        return legalCaseRepository.findByTitleContainingOrContentContaining(keyword, keyword, pageable);
    }
    
    public List<LegalCase> getCasesByLawType(String lawType) {
        return legalCaseRepository.findByLawType(lawType);
    }
    
    public List<LegalCase> getCasesByCaseType(String caseType) {
        return legalCaseRepository.findByCaseType(caseType);
    }
    
    public Optional<LegalCase> getCaseById(Long id) {
        return legalCaseRepository.findById(id);
    }
    
    @Transactional
    public LegalCase saveCase(LegalCase legalCase) {
        return legalCaseRepository.save(legalCase);
    }
    
    @Transactional
    public void deleteCase(Long id) {
        legalCaseRepository.deleteById(id);
    }
}

