package com.pru.data;

import java.net.Inet4Address;
import java.net.InetAddress;

public class Entry {
    private String emailHash;
    private String ipAddress;

    public Entry(){
    }

    public Entry(String emailHash, String ipAddress) {
        this.emailHash = emailHash;
        this.ipAddress = ipAddress;
    }

    public void updateEntry(String fromUser){
        //TODO
        //PARSE DO JSON?
    }


}
