package com.legal.service;

import com.alibaba.fastjson2.JSON;
import com.legal.entity.KnowledgeBase;
import com.legal.entity.LegalArticle;
import com.legal.entity.LegalCase;
import com.legal.entity.LegalConcept;
import com.legal.entity.QuestionAnswer;
import com.legal.repository.KnowledgeBaseRepository;
import com.legal.repository.LegalArticleRepository;
import com.legal.repository.LegalCaseRepository;
import com.legal.repository.LegalConceptRepository;
import com.legal.repository.QuestionAnswerRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@Service
public class QuestionAnswerService {
    
    @Autowired
    private QuestionAnswerRepository questionAnswerRepository;
    
    @Autowired
    private DeepSeekService deepSeekService;
    
    @Autowired
    private KnowledgeBaseRepository knowledgeBaseRepository;
    
    @Autowired
    private LegalArticleRepository legalArticleRepository;
    
    @Autowired
    private LegalCaseRepository legalCaseRepository;
    
    @Autowired
    private LegalConceptRepository legalConceptRepository;
    
    /**
     * 处理用户问题并生成答案
     */
    @Transactional
    public Map<String, Object> processQuestion(String question, Long userId, String sessionId) {
        Map<String, Object> result = new HashMap<>();
        
        // 1. 问题分类
        String questionType = deepSeekService.classifyQuestion(question);
        
        // 2. 实体识别
        Map<String, List<String>> entities = deepSeekService.extractEntities(question);
        
        // 3. 知识检索
        String context = retrieveKnowledge(question, questionType, entities);
        
        // 4. 生成答案
        String answer = deepSeekService.generateAnswer(question, context);
        
        // 5. 可信度评估
        Double confidenceScore = deepSeekService.evaluateConfidence(question, answer);
        
        // 6. 检索相关法条和案例
        List<LegalArticle> relatedLaws = findRelatedLaws(question, entities);
        List<LegalCase> relatedCases = findRelatedCases(question, questionType);
        
        // 7. 保存问答记录
        QuestionAnswer qa = new QuestionAnswer();
        qa.setUserId(userId);
        qa.setQuestion(question);
        qa.setAnswer(answer);
        qa.setQuestionType(questionType);
        qa.setConfidenceScore(confidenceScore);
        qa.setEntities(JSON.toJSONString(entities));
        qa.setRelatedLaws(JSON.toJSONString(relatedLaws.stream()
                .map(la -> la.getTitle() + "第" + la.getArticleNumber() + "条")
                .collect(Collectors.toList())));
        qa.setRelatedCases(JSON.toJSONString(relatedCases.stream()
                .map(lc -> lc.getTitle())
                .collect(Collectors.toList())));
        qa.setSessionId(sessionId);
        qa.setIsFeedback(false);
        qa = questionAnswerRepository.save(qa);
        
        // 8. 构建返回结果
        result.put("id", qa.getId());
        result.put("question", question);
        result.put("answer", answer);
        result.put("questionType", questionType);
        result.put("confidenceScore", confidenceScore);
        result.put("entities", entities);
        result.put("relatedLaws", relatedLaws);
        result.put("relatedCases", relatedCases);
        result.put("sessionId", sessionId);
        
        return result;
    }
    
    /**
     * 知识检索
     */
    private String retrieveKnowledge(String question, String questionType, Map<String, List<String>> entities) {
        StringBuilder context = new StringBuilder();
        
        // 1. 从知识库检索相似问题
        List<KnowledgeBase> similarQAs = knowledgeBaseRepository
                .searchByKeywordOrderByScore(question, org.springframework.data.domain.PageRequest.of(0, 3));
        if (!similarQAs.isEmpty()) {
            context.append("相关问答：\n");
            for (KnowledgeBase kb : similarQAs) {
                context.append("Q: ").append(kb.getQuestion()).append("\n");
                context.append("A: ").append(kb.getAnswer()).append("\n\n");
            }
        }
        
        // 2. 检索相关法条
        List<String> laws = entities.getOrDefault("laws", new ArrayList<>());
        for (String law : laws) {
            List<LegalArticle> articles = legalArticleRepository.searchByKeyword(law);
            if (!articles.isEmpty()) {
                context.append("相关法条：\n");
                for (LegalArticle article : articles.subList(0, Math.min(3, articles.size()))) {
                    context.append(article.getTitle())
                            .append("第").append(article.getArticleNumber())
                            .append("条：").append(article.getContent()).append("\n\n");
                }
            }
        }
        
        // 3. 检索法律概念
        List<String> concepts = entities.getOrDefault("concepts", new ArrayList<>());
        for (String concept : concepts) {
            Optional<LegalConcept> legalConcept = legalConceptRepository.findByName(concept);
            if (legalConcept.isPresent()) {
                context.append("概念定义：").append(legalConcept.get().getName())
                        .append(" - ").append(legalConcept.get().getDefinition()).append("\n\n");
            }
        }
        
        return context.toString();
    }
    
    /**
     * 查找相关法条
     */
    private List<LegalArticle> findRelatedLaws(String question, Map<String, List<String>> entities) {
        List<LegalArticle> laws = new ArrayList<>();
        
        // 根据实体查找
        List<String> lawNames = entities.getOrDefault("laws", new ArrayList<>());
        for (String lawName : lawNames) {
            laws.addAll(legalArticleRepository.searchByKeyword(lawName));
        }
        
        // 根据问题关键词查找
        if (laws.isEmpty()) {
            laws.addAll(legalArticleRepository.searchByKeyword(question));
        }
        
        return laws.stream().distinct().limit(5).collect(Collectors.toList());
    }
    
    /**
     * 查找相关案例
     */
    private List<LegalCase> findRelatedCases(String question, String questionType) {
        List<LegalCase> cases = legalCaseRepository.searchByKeyword(question);
        if (cases.isEmpty() && questionType != null) {
            cases = legalCaseRepository.findByCaseType(questionType);
        }
        return cases.stream().distinct().limit(3).collect(Collectors.toList());
    }
    
    /**
     * 获取问答历史
     */
    public Page<QuestionAnswer> getQuestionHistory(Long userId, Pageable pageable) {
        return questionAnswerRepository.findByUserId(userId, pageable);
    }
    
    /**
     * 根据会话ID获取对话历史
     */
    public List<QuestionAnswer> getConversationHistory(String sessionId) {
        return questionAnswerRepository.findBySessionId(sessionId);
    }
    
    /**
     * 提交反馈
     */
    @Transactional
    public void submitFeedback(Long qaId, String feedbackType) {
        QuestionAnswer qa = questionAnswerRepository.findById(qaId)
                .orElseThrow(() -> new RuntimeException("问答记录不存在"));
        qa.setIsFeedback(true);
        qa.setFeedbackType(feedbackType);
        questionAnswerRepository.save(qa);
    }
    
    /**
     * 搜索问答记录
     */
    public Page<QuestionAnswer> searchQuestions(String keyword, Pageable pageable) {
        return questionAnswerRepository.findByQuestionContaining(keyword, pageable);
    }
}

