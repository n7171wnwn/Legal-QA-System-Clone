package com.legal.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "question_answers")
public class QuestionAnswer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user_id")
    private Long userId;

    @Column(nullable = false, length = 2000)
    private String question;

    @Column(length = 5000)
    private String answer;

    @Column(name = "question_type")
    private String questionType; // 法条查询、概念定义、程序咨询、案例分析

    @Column(name = "confidence_score")
    private Double confidenceScore; // 可信度评分 0-1

    @Column(name = "entities", length = 1000)
    private String entities; // JSON格式存储识别的实体

    @Column(name = "related_laws", length = 1000)
    private String relatedLaws; // 相关法条

    @Column(name = "related_cases", length = 1000)
    private String relatedCases; // 相关案例

    @Column(name = "session_id")
    private String sessionId; // 会话ID，用于多轮对话

    @Column(name = "is_feedback")
    private Boolean isFeedback; // 是否有反馈

    @Column(name = "feedback_type")
    private String feedbackType; // positive, negative

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @PrePersist
    protected void onCreate() {
        createTime = LocalDateTime.now();
    }
}

