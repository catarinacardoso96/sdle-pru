package com.pru.util;

public class PeerAnswer {
    private String hash;
    private boolean answer;

    public PeerAnswer(String hash, boolean answer){
        this.answer = answer;
        this.hash = hash;
    }

    public String getHash(){
        return this.hash;
    }

    public boolean isAnswer() {
        return answer;
    }

    public void setAnswer(boolean answer){
        this.answer = answer;
    }
}

