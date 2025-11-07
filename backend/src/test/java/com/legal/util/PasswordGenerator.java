package com.legal.util;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 * 密码哈希生成工具
 * 用于生成BCrypt密码哈希，用于数据库初始化
 */
public class PasswordGenerator {
    public static void main(String[] args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        
        String password = "123456";
        String encodedPassword = encoder.encode(password);
        
        System.out.println("原始密码: " + password);
        System.out.println("BCrypt哈希: " + encodedPassword);
        System.out.println();
        
        // 验证哈希是否正确
        boolean matches = encoder.matches(password, encodedPassword);
        System.out.println("验证结果: " + (matches ? "✓ 正确" : "✗ 错误"));
        System.out.println();
        
        // 验证脚本中的哈希
        String scriptHash = "$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iwK8pQMW";
        boolean scriptMatches = encoder.matches(password, scriptHash);
        System.out.println("脚本中的哈希验证: " + (scriptMatches ? "✓ 正确" : "✗ 错误"));
        System.out.println();
        
        // 生成SQL语句
        System.out.println("SQL插入语句:");
        System.out.println("INSERT INTO users (username, password, nickname, user_type) VALUES");
        System.out.println("('admin', '" + encodedPassword + "', '管理员', 1),");
        System.out.println("('user1', '" + encodedPassword + "', '测试用户', 0);");
    }
}

