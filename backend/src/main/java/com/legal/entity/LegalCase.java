package com.legal.entity;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "legal_cases")
public class LegalCase {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title; // 案例标题

    @Column(name = "case_type")
    private String caseType; // 案由

    @Column(length = 5000)
    private String content; // 案例内容

    @Column(name = "court_name")
    private String courtName; // 审理法院

    @Column(name = "judge_date")
    private LocalDateTime judgeDate; // 判决日期

    @Column(name = "dispute_point", length = 2000)
    private String disputePoint; // 核心争议点

    @Column(name = "judgment_result", length = 2000)
    private String judgmentResult; // 判决结果

    @Column(name = "law_type")
    private String lawType; // 法律领域

    @Column(name = "create_time")
    private LocalDateTime createTime;

    @PrePersist
    protected void onCreate() {
        createTime = LocalDateTime.now();
    }
}

