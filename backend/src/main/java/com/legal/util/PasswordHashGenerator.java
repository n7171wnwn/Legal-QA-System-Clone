package com.legal.util;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 * 密码哈希生成工具类
 * 用于生成和验证BCrypt密码哈希
 */
public class PasswordHashGenerator {
    
    public static void main(String[] args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        
        // 要加密的密码
        String password = "123456";
        
        // 生成新的哈希
        String newHash = encoder.encode(password);
        System.out.println("============================================");
        System.out.println("密码哈希生成工具");
        System.out.println("============================================");
        System.out.println("原始密码: " + password);
        System.out.println("新生成的BCrypt哈希: " + newHash);
        System.out.println();
        
        // 验证新生成的哈希
        boolean newMatches = encoder.matches(password, newHash);
        System.out.println("新哈希验证: " + (newMatches ? "✓ 正确" : "✗ 错误"));
        System.out.println();
        
        // 验证脚本中的旧哈希
        String oldHash = "$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iwK8pQMW";
        boolean oldMatches = encoder.matches(password, oldHash);
        System.out.println("脚本中的旧哈希: " + oldHash);
        System.out.println("旧哈希验证: " + (oldMatches ? "✓ 正确" : "✗ 错误"));
        System.out.println();
        
        // 生成SQL更新语句
        System.out.println("============================================");
        System.out.println("SQL更新语句（如果旧哈希不正确）:");
        System.out.println("============================================");
        System.out.println("UPDATE users SET password = '" + newHash + "' WHERE username = 'admin';");
        System.out.println("UPDATE users SET password = '" + newHash + "' WHERE username = 'user1';");
        System.out.println();
        
        System.out.println("============================================");
        System.out.println("SQL插入语句（新用户）:");
        System.out.println("============================================");
        System.out.println("INSERT INTO users (username, password, nickname, user_type) VALUES");
        System.out.println("('admin', '" + newHash + "', '管理员', 1),");
        System.out.println("('user1', '" + newHash + "', '测试用户', 0);");
    }
}

