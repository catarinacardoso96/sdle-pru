package com.pru.data;

import com.pru.util.Util;

import java.nio.channels.AsynchronousSocketChannel;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Catalog {
    private Map<String, Entry> onlinePeers;

    public Catalog() {
        onlinePeers = new HashMap<>();
    }

    public String onlineUser() {
        String users = Util.getRandomPeers(onlinePeers);
        return users;
    }

    public void offlineUser() {
        //o que fazer aqui?
    }
}
