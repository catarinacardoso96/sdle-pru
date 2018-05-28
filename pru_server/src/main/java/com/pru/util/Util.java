package com.pru.util;

import com.google.gson.Gson;
import com.pru.data.Entry;


import java.util.*;

public class Util {

    public static String getRandomPeers(String senderPeer, Map<String, Entry> onlineUsers) {
        Gson gson = new Gson();
        Set<Entry> usersToConnect = new HashSet<>();
        List<String> users = new ArrayList<>(onlineUsers.keySet());
        users.remove(senderPeer);
        if(users.size() == 0){
            return gson.toJson("USERS ONLINE NOT FOUNDED");
        }
        int sizeOn = users.size();
        int anotherUser = -1;
        int userToConnect = new Random().nextInt(sizeOn);
        Entry firstUser = onlineUsers.get(users.get(userToConnect));
        users.remove(users.get(userToConnect));
        Entry secondUser;
        if(sizeOn > 1){
            anotherUser = new Random().nextInt(sizeOn);
            secondUser = onlineUsers.get(users.get(anotherUser));
            users.remove(users.get(anotherUser));
            usersToConnect.add(secondUser);
        }
        usersToConnect.add(firstUser);

        String jsonToSend = gson.toJson(usersToConnect);

        return jsonToSend;
    }
}
