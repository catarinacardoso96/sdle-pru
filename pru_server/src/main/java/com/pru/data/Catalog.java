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

    public void onlineUser() {
        List<Entry> users = Util.getRandomPeers(onlinePeers);
    }

    public void offlineUser() {

    }
}
