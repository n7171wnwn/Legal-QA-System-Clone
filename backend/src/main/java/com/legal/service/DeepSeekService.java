package com.legal.service;

import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONArray;
import com.alibaba.fastjson2.JSONObject;
import com.legal.config.DeepSeekConfig;
import lombok.extern.slf4j.Slf4j;
import okhttp3.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Slf4j
@Service
public class DeepSeekService {
    
    @Autowired
    private DeepSeekConfig deepSeekConfig;
    
    private final OkHttpClient httpClient;
    
    public DeepSeekService() {
        this.httpClient = new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(60, TimeUnit.SECONDS)
                .writeTimeout(60, TimeUnit.SECONDS)
                .build();
    }
    
    /**
     * 调用DeepSeek API生成答案
     */
    public String generateAnswer(String question, String context) {
        try {
            JSONObject requestBody = new JSONObject();
            requestBody.put("model", deepSeekConfig.getModel());
            
            JSONArray messages = new JSONArray();
            
            // 系统提示词
            JSONObject systemMessage = new JSONObject();
            systemMessage.put("role", "system");
            systemMessage.put("content", buildSystemPrompt(context));
            messages.add(systemMessage);
            
            // 用户问题
            JSONObject userMessage = new JSONObject();
            userMessage.put("role", "user");
            userMessage.put("content", question);
            messages.add(userMessage);
            
            requestBody.put("messages", messages);
            requestBody.put("temperature", 0.7);
            requestBody.put("max_tokens", 2000);
            
            Request request = new Request.Builder()
                    .url(deepSeekConfig.getUrl())
                    .addHeader("Content-Type", "application/json")
                    .addHeader("Authorization", "Bearer " + deepSeekConfig.getApiKey())
                    .post(RequestBody.create(requestBody.toJSONString(), MediaType.parse("application/json")))
                    .build();
            
            try (Response response = httpClient.newCall(request).execute()) {
                if (!response.isSuccessful()) {
                    log.error("DeepSeek API调用失败: {}", response.code());
                    return "抱歉，服务暂时不可用，请稍后再试。";
                }
                
                String responseBody = response.body().string();
                JSONObject jsonResponse = JSON.parseObject(responseBody);
                JSONArray choices = jsonResponse.getJSONArray("choices");
                
                if (choices != null && choices.size() > 0) {
                    JSONObject choice = choices.getJSONObject(0);
                    JSONObject message = choice.getJSONObject("message");
                    return message.getString("content");
                }
            }
        } catch (IOException e) {
            log.error("调用DeepSeek API异常", e);
        }
        
        return "抱歉，生成答案时出现错误，请稍后再试。";
    }
    
    /**
     * 构建系统提示词
     */
    private String buildSystemPrompt(String context) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("你是一位专业的法律咨询AI助手，具有丰富的法律知识和司法实践经验。");
        prompt.append("你的任务是回答用户的法律问题，提供准确、专业、易懂的法律建议。");
        prompt.append("\n\n");
        prompt.append("回答要求：");
        prompt.append("1. 回答要准确、专业，基于中国法律法规");
        prompt.append("2. 语言要通俗易懂，避免过于专业的术语");
        prompt.append("3. 如果涉及具体法条，要明确指出法条名称和条号");
        prompt.append("4. 如果是案例分析，要提供相关案例参考");
        prompt.append("5. 如果问题不够明确，要主动询问以获取更多信息");
        prompt.append("\n\n");
        
        if (context != null && !context.isEmpty()) {
            prompt.append("相关知识上下文：\n");
            prompt.append(context);
            prompt.append("\n\n");
        }
        
        prompt.append("请根据以上要求回答用户的问题。");
        
        return prompt.toString();
    }
    
    /**
     * 问题分类
     */
    public String classifyQuestion(String question) {
        String prompt = "请对以下法律问题进行分类，只返回类别名称（法条查询、概念定义、程序咨询、案例分析、其他）：\n" + question;
        String result = generateAnswer(prompt, null);
        return extractCategory(result);
    }
    
    /**
     * 实体识别
     */
    public Map<String, List<String>> extractEntities(String question) {
        String prompt = "请从以下法律问题中识别实体，包括：法条名称、罪名、机构名称、法律概念等。"
                + "返回JSON格式：{\"laws\":[],\"crimes\":[],\"organizations\":[],\"concepts\":[]}\n"
                + "问题：" + question;
        
        String result = generateAnswer(prompt, null);
        return parseEntities(result);
    }
    
    /**
     * 评估答案可信度
     */
    public Double evaluateConfidence(String question, String answer) {
        // 简单实现：基于答案长度、是否包含法条引用等因素
        double score = 0.5;
        
        if (answer.length() > 100) {
            score += 0.2;
        }
        
        if (answer.contains("《") && answer.contains("》")) {
            score += 0.2;
        }
        
        if (answer.contains("第") && answer.contains("条")) {
            score += 0.1;
        }
        
        return Math.min(score, 1.0);
    }
    
    private String extractCategory(String result) {
        if (result.contains("法条查询")) return "法条查询";
        if (result.contains("概念定义")) return "概念定义";
        if (result.contains("程序咨询")) return "程序咨询";
        if (result.contains("案例分析")) return "案例分析";
        return "其他";
    }
    
    private Map<String, List<String>> parseEntities(String result) {
        Map<String, List<String>> entities = new HashMap<>();
        entities.put("laws", new ArrayList<>());
        entities.put("crimes", new ArrayList<>());
        entities.put("organizations", new ArrayList<>());
        entities.put("concepts", new ArrayList<>());
        
        try {
            JSONObject json = JSON.parseObject(result);
            if (json != null) {
                entities.put("laws", json.getJSONArray("laws") != null ? 
                    json.getJSONArray("laws").toJavaList(String.class) : new ArrayList<>());
                entities.put("crimes", json.getJSONArray("crimes") != null ? 
                    json.getJSONArray("crimes").toJavaList(String.class) : new ArrayList<>());
                entities.put("organizations", json.getJSONArray("organizations") != null ? 
                    json.getJSONArray("organizations").toJavaList(String.class) : new ArrayList<>());
                entities.put("concepts", json.getJSONArray("concepts") != null ? 
                    json.getJSONArray("concepts").toJavaList(String.class) : new ArrayList<>());
            }
        } catch (Exception e) {
            log.warn("解析实体失败", e);
        }
        
        return entities;
    }
}

