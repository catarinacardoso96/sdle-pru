package com.pru.util;

import com.google.gson.Gson;
import com.pru.data.Entry;


import java.util.*;

public class Util {

    public static String getRandomPeers(String senderPeer, Map<String, Entry> onlineUsers) {
        Gson gson = new Gson();
        int maximumConns = 3;
        if(onlineUsers.size() - 1 <= maximumConns){
            maximumConns = onlineUsers.size()-1;
        }
        Set<Entry> usersToConnect = new HashSet<>();
        List<String> users = new ArrayList<>(onlineUsers.keySet());
        users.remove(senderPeer);
        if(users.size() == 0){
            return gson.toJson("");
        }
        int sizeOn = users.size();
        int userToConnect;
        while(maximumConns > 0){
            userToConnect = new Random().nextInt(sizeOn);
            Entry firstUser = onlineUsers.get(users.get(userToConnect));
            users.remove(users.get(userToConnect));
            usersToConnect.add(firstUser);
            sizeOn--;
            maximumConns--;
        }

        String jsonToSend = gson.toJson(usersToConnect);

        return jsonToSend;
    }
}
