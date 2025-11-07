package com.legal.repository;

import com.legal.entity.QuestionAnswer;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface QuestionAnswerRepository extends JpaRepository<QuestionAnswer, Long> {
    Page<QuestionAnswer> findByUserId(Long userId, Pageable pageable);
    List<QuestionAnswer> findBySessionId(String sessionId);
    Page<QuestionAnswer> findByQuestionContaining(String keyword, Pageable pageable);
    
    @Query("SELECT COUNT(q) FROM QuestionAnswer q WHERE DATE(q.createTime) = CURRENT_DATE")
    Long countTodayQuestions();
    
    @Query("SELECT q.questionType, COUNT(q) FROM QuestionAnswer q GROUP BY q.questionType")
    List<Object[]> countByQuestionType();
}

