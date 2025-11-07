package com.legal.repository;

import com.legal.entity.LegalCase;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface LegalCaseRepository extends JpaRepository<LegalCase, Long> {
    Page<LegalCase> findByTitleContainingOrContentContaining(String title, String content, Pageable pageable);
    List<LegalCase> findByLawType(String lawType);
    List<LegalCase> findByCaseType(String caseType);
    
    @Query("SELECT lc FROM LegalCase lc WHERE lc.title LIKE %?1% OR lc.disputePoint LIKE %?1%")
    List<LegalCase> searchByKeyword(String keyword);
}

