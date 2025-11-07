package com.legal.repository;

import com.legal.entity.KnowledgeBase;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface KnowledgeBaseRepository extends JpaRepository<KnowledgeBase, Long> {
    Page<KnowledgeBase> findByQuestionContainingOrAnswerContaining(String question, String answer, Pageable pageable);
    List<KnowledgeBase> findByQuestionType(String questionType);
    List<KnowledgeBase> findByLawType(String lawType);
    
    @Query("SELECT kb FROM KnowledgeBase kb WHERE kb.question LIKE %?1% OR kb.answer LIKE %?1% ORDER BY kb.qualityScore DESC")
    List<KnowledgeBase> searchByKeywordOrderByScore(String keyword, Pageable pageable);
}

