package com.pru.data;

public class Entry {
    private String ip;
    private int port;

    public Entry(){
    }

    public Entry(String ipAddress, int port) {
        this.port = port;
        this.ip = ipAddress;
    }

    public String getIp(){
        return this.ip;
    }

    public int getPort() {
        return this.port;
    }



}
