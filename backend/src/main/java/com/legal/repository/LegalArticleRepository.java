package com.legal.repository;

import com.legal.entity.LegalArticle;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface LegalArticleRepository extends JpaRepository<LegalArticle, Long> {
    Page<LegalArticle> findByTitleContainingOrContentContaining(String title, String content, Pageable pageable);
    List<LegalArticle> findByLawType(String lawType);
    List<LegalArticle> findByIsValidTrue();
    
    @Query("SELECT la FROM LegalArticle la WHERE la.title LIKE %?1% OR la.articleNumber LIKE %?1%")
    List<LegalArticle> searchByKeyword(String keyword);
}

