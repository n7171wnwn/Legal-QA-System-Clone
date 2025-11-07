package com.legal.service;

import com.legal.entity.LegalConcept;
import com.legal.repository.LegalConceptRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class LegalConceptService {
    
    @Autowired
    private LegalConceptRepository legalConceptRepository;
    
    public Page<LegalConcept> searchConcepts(String keyword, Pageable pageable) {
        return legalConceptRepository.findByNameContainingOrDefinitionContaining(keyword, keyword, pageable);
    }
    
    public List<LegalConcept> getConceptsByLawType(String lawType) {
        return legalConceptRepository.findByLawType(lawType);
    }
    
    public Optional<LegalConcept> getConceptByName(String name) {
        return legalConceptRepository.findByName(name);
    }
    
    public Optional<LegalConcept> getConceptById(Long id) {
        return legalConceptRepository.findById(id);
    }
    
    @Transactional
    public LegalConcept saveConcept(LegalConcept concept) {
        return legalConceptRepository.save(concept);
    }
    
    @Transactional
    public void deleteConcept(Long id) {
        legalConceptRepository.deleteById(id);
    }
}

