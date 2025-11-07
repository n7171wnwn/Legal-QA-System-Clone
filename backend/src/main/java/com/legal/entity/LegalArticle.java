package com.legal.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "legal_articles")
public class LegalArticle {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title; // 法律名称

    @Column(name = "article_number")
    private String articleNumber; // 条号

    @Column(length = 5000)
    private String content; // 条文内容

    @Column(name = "law_type")
    private String lawType; // 民法、刑法、行政法等

    @Column(name = "publish_org")
    private String publishOrg; // 发布机构

    @Column(name = "publish_date")
    private LocalDateTime publishDate;

    @Column(name = "is_valid")
    private Boolean isValid; // 是否有效

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    @PrePersist
    protected void onCreate() {
        createTime = LocalDateTime.now();
        updateTime = LocalDateTime.now();
        if (isValid == null) {
            isValid = true;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        updateTime = LocalDateTime.now();
    }
}

