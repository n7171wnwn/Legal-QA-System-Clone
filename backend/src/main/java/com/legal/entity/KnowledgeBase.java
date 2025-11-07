package com.legal.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "knowledge_base")
public class KnowledgeBase {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String question;

    @Column(nullable = false, length = 5000)
    private String answer;

    @Column(name = "question_type")
    private String questionType;

    @Column(name = "tags", length = 500)
    private String tags; // 标签，逗号分隔

    @Column(name = "law_type")
    private String lawType;

    @Column(name = "usage_count")
    private Integer usageCount; // 使用次数

    @Column(name = "quality_score")
    private Double qualityScore; // 质量评分

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    @PrePersist
    protected void onCreate() {
        createTime = LocalDateTime.now();
        updateTime = LocalDateTime.now();
        if (usageCount == null) {
            usageCount = 0;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        updateTime = LocalDateTime.now();
    }
}

