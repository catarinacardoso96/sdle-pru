package com.pru.data;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.pru.util.PeerAnswer;
import com.pru.util.Util;

import java.lang.reflect.Type;
import java.nio.channels.AsynchronousSocketChannel;
import java.util.*;

public class Catalog {
    private Map<String, Entry> onlinePeers;
    private Map<String, Entry> offlinePeers;

    public Catalog() {
        onlinePeers = new HashMap<>();
        offlinePeers = new HashMap<>();
    }

    public String onlineUser(String senderPeer) {
        String users = Util.getRandomPeers(senderPeer, onlinePeers);
        return users;
    }

    public PeerAnswer update(String s){
        Gson gson = new Gson();
        Map<String, Object> jsonInput = gson.fromJson(s, (Type) Map.class);
        String hash = (String) jsonInput.get("hash");
        PeerAnswer peerAnswer = new PeerAnswer(hash, true);
        if(jsonInput.containsKey("ip")){
            String ip = (String) jsonInput.get("ip");
            double port  = (double) jsonInput.get("port");
            Entry en = new Entry(ip, (int) port);
            this.onlinePeers.put(hash, en);
        }else{
            Entry e = this.onlinePeers.get(hash);
            this.offlinePeers.put(hash, e);
            this.onlinePeers.remove(hash);
            peerAnswer.setAnswer(false);
        }
        return peerAnswer;
    }


}
