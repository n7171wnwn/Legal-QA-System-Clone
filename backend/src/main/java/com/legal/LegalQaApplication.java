package com.legal;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class LegalQaApplication {
    public static void main(String[] args) {
        SpringApplication.run(LegalQaApplication.class, args);
    }
}

