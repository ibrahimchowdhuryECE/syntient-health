package com.clinic.orch.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.util.Map;

public class TurnRequest {
    @NotBlank(message = "conversation_id is required")
    @JsonProperty("conversation_id")
    private String conversationId;

    @NotBlank(message = "turn_id is required")
    @JsonProperty("turn_id")
    private String turnId;

    @NotNull(message = "payload is required")
    @Valid
    private TurnPayload payload;

    // Constructors
    public TurnRequest() {}

    public TurnRequest(String conversationId, String turnId, TurnPayload payload) {
        this.conversationId = conversationId;
        this.turnId = turnId;
        this.payload = payload;
    }

    // Getters and Setters
    public String getConversationId() {
        return conversationId;
    }

    public void setConversationId(String conversationId) {
        this.conversationId = conversationId;
    }

    public String getTurnId() {
        return turnId;
    }

    public void setTurnId(String turnId) {
        this.turnId = turnId;
    }

    public TurnPayload getPayload() {
        return payload;
    }

    public void setPayload(TurnPayload payload) {
        this.payload = payload;
    }

    public static class TurnPayload {
        @NotBlank(message = "patient_id is required")
        @JsonProperty("patient_id")
        private String patientId;

        @NotBlank(message = "presenting_complaint is required")
        @JsonProperty("presenting_complaint")
        private String presentingComplaint;

        @NotNull(message = "fields is required")
        private Map<String, Object> fields;

        @JsonProperty("free_text")
        private String freeText;

        // Constructors
        public TurnPayload() {}

        public TurnPayload(String patientId, String presentingComplaint, Map<String, Object> fields, String freeText) {
            this.patientId = patientId;
            this.presentingComplaint = presentingComplaint;
            this.fields = fields;
            this.freeText = freeText;
        }

        // Getters and Setters
        public String getPatientId() {
            return patientId;
        }

        public void setPatientId(String patientId) {
            this.patientId = patientId;
        }

        public String getPresentingComplaint() {
            return presentingComplaint;
        }

        public void setPresentingComplaint(String presentingComplaint) {
            this.presentingComplaint = presentingComplaint;
        }

        public Map<String, Object> getFields() {
            return fields;
        }

        public void setFields(Map<String, Object> fields) {
            this.fields = fields;
        }

        public String getFreeText() {
            return freeText;
        }

        public void setFreeText(String freeText) {
            this.freeText = freeText;
        }
    }
}
