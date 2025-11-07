package com.legal.controller;

import com.legal.dto.ApiResponse;
import com.legal.dto.LoginRequest;
import com.legal.dto.RegisterRequest;
import com.legal.entity.User;
import com.legal.service.UserService;
import com.legal.util.JwtUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/auth")
@CrossOrigin
public class AuthController {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private JwtUtil jwtUtil;
    
    @Autowired
    private BCryptPasswordEncoder passwordEncoder;
    
    @PostMapping("/register")
    public ApiResponse<Map<String, Object>> register(@RequestBody RegisterRequest request) {
        try {
            if (userService.existsByUsername(request.getUsername())) {
                return ApiResponse.error("用户名已存在");
            }
            
            User user = new User();
            user.setUsername(request.getUsername());
            user.setPassword(passwordEncoder.encode(request.getPassword()));
            user.setEmail(request.getEmail());
            user.setPhone(request.getPhone());
            user.setNickname(request.getNickname());
            user.setUserType(0); // 普通用户
            
            user = userService.saveUser(user);
            
            String token = jwtUtil.generateToken(user.getUsername(), user.getId());
            
            Map<String, Object> result = new HashMap<>();
            result.put("token", token);
            result.put("user", user);
            
            return ApiResponse.success("注册成功", result);
        } catch (Exception e) {
            log.error("注册失败", e);
            return ApiResponse.error("注册失败：" + e.getMessage());
        }
    }
    
    @PostMapping("/login")
    public ApiResponse<Map<String, Object>> login(@RequestBody LoginRequest request) {
        try {
            User user = userService.findByUsername(request.getUsername())
                    .orElseThrow(() -> new RuntimeException("用户不存在"));
            
            if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                return ApiResponse.error("密码错误");
            }
            
            String token = jwtUtil.generateToken(user.getUsername(), user.getId());
            
            Map<String, Object> result = new HashMap<>();
            result.put("token", token);
            result.put("user", user);
            
            return ApiResponse.success("登录成功", result);
        } catch (Exception e) {
            log.error("登录失败", e);
            return ApiResponse.error("登录失败：" + e.getMessage());
        }
    }
}

