package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.service.QuestionAnswerService;
import com.legal.util.JwtUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/qa")
@CrossOrigin
public class QuestionAnswerController {
    
    @Autowired
    private QuestionAnswerService questionAnswerService;
    
    @Autowired
    private JwtUtil jwtUtil;
    
    /**
     * 提问
     */
    @PostMapping("/ask")
    public ApiResponse<Map<String, Object>> askQuestion(
            @RequestBody Map<String, String> request,
            HttpServletRequest httpRequest) {
        try {
            String question = request.get("question");
            String sessionId = request.getOrDefault("sessionId", generateSessionId());
            
            String token = httpRequest.getHeader("Authorization");
            Long userId = null;
            if (token != null && token.startsWith("Bearer ")) {
                token = token.substring(7);
                if (jwtUtil.validateToken(token)) {
                    userId = jwtUtil.getUserIdFromToken(token);
                }
            }
            
            Map<String, Object> result = questionAnswerService.processQuestion(question, userId, sessionId);
            return ApiResponse.success(result);
        } catch (Exception e) {
            log.error("处理问题失败", e);
            return ApiResponse.error("处理问题失败：" + e.getMessage());
        }
    }
    
    /**
     * 获取问答历史
     */
    @GetMapping("/history")
    public ApiResponse<Page<?>> getHistory(
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            HttpServletRequest request) {
        try {
            String token = request.getHeader("Authorization");
            if (token == null || !token.startsWith("Bearer ")) {
                return ApiResponse.error(401, "未登录");
            }
            
            token = token.substring(7);
            if (!jwtUtil.validateToken(token)) {
                return ApiResponse.error(401, "Token无效");
            }
            
            Long userId = jwtUtil.getUserIdFromToken(token);
            Pageable pageable = PageRequest.of(page, size);
            Page<?> history = questionAnswerService.getQuestionHistory(userId, pageable);
            return ApiResponse.success(history);
        } catch (Exception e) {
            log.error("获取历史失败", e);
            return ApiResponse.error("获取历史失败：" + e.getMessage());
        }
    }
    
    /**
     * 获取会话历史
     */
    @GetMapping("/conversation/{sessionId}")
    public ApiResponse<?> getConversation(@PathVariable String sessionId) {
        try {
            return ApiResponse.success(questionAnswerService.getConversationHistory(sessionId));
        } catch (Exception e) {
            log.error("获取会话历史失败", e);
            return ApiResponse.error("获取会话历史失败：" + e.getMessage());
        }
    }
    
    /**
     * 提交反馈
     */
    @PostMapping("/feedback")
    public ApiResponse<?> submitFeedback(@RequestBody Map<String, Object> request) {
        try {
            Long qaId = Long.valueOf(request.get("qaId").toString());
            String feedbackType = request.get("feedbackType").toString();
            questionAnswerService.submitFeedback(qaId, feedbackType);
            return ApiResponse.success("反馈提交成功");
        } catch (Exception e) {
            log.error("提交反馈失败", e);
            return ApiResponse.error("提交反馈失败：" + e.getMessage());
        }
    }
    
    private String generateSessionId() {
        return "session_" + System.currentTimeMillis() + "_" + (int)(Math.random() * 1000);
    }
}

