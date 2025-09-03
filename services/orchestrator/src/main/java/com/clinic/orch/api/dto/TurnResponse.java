package com.clinic.orch.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class TurnResponse {
    private String route;
    
    @JsonProperty("booking_window")
    private String bookingWindow;
    
    private String prompt;

    // Constructors
    public TurnResponse() {}

    public TurnResponse(String route) {
        this.route = route;
    }

    public TurnResponse(String route, String bookingWindow, String prompt) {
        this.route = route;
        this.bookingWindow = bookingWindow;
        this.prompt = prompt;
    }

    // Getters and Setters
    public String getRoute() {
        return route;
    }

    public void setRoute(String route) {
        this.route = route;
    }

    public String getBookingWindow() {
        return bookingWindow;
    }

    public void setBookingWindow(String bookingWindow) {
        this.bookingWindow = bookingWindow;
    }

    public String getPrompt() {
        return prompt;
    }

    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }
}
