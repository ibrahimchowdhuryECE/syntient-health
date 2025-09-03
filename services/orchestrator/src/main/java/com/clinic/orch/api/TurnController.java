package com.clinic.orch.api;

import com.clinic.orch.api.dto.TurnRequest;
import com.clinic.orch.api.dto.TurnResponse;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/orch")
public class TurnController {

    @PostMapping("/turn")
    public ResponseEntity<TurnResponse> processTurn(@Valid @RequestBody TurnRequest request) {
        // Stub implementation - returns static response
        // TODO: Implement actual business logic
        
        TurnResponse response = new TurnResponse();
        response.setRoute("ASK");
        response.setPrompt("Has the chest pain lasted more than 15 minutes?");
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "healthy");
        health.put("timestamp", LocalDateTime.now().toString());
        health.put("service", "orchestrator");
        
        return ResponseEntity.ok(health);
    }
}
