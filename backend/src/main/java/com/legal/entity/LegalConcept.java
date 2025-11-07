package com.legal.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "legal_concepts")
public class LegalConcept {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name; // 概念名称

    @Column(length = 2000)
    private String definition; // 定义

    @Column(length = 5000)
    private String explanation; // 详细解释

    @Column(name = "law_type")
    private String lawType; // 所属法律领域

    @Column(name = "related_concepts", length = 1000)
    private String relatedConcepts; // 相关概念

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    @PrePersist
    protected void onCreate() {
        createTime = LocalDateTime.now();
        updateTime = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updateTime = LocalDateTime.now();
    }
}

