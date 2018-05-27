package com.pru.util;

import com.google.gson.Gson;
import com.pru.data.Entry;


import java.util.*;

public class Util {

    public static String getRandomPeers(Map<String, Entry> onlineUsers) {
        int sizeOn = onlineUsers.size();
        int userToConnect = new Random().nextInt(sizeOn);
        int anotherUser = new Random().nextInt(sizeOn);
        while(userToConnect == anotherUser){
            anotherUser = new Random().nextInt(sizeOn);
        }

        Set<Entry> usersToConnect = new HashSet<>();
        usersToConnect.add(onlineUsers.get(usersToConnect));
        usersToConnect.add(onlineUsers.get(anotherUser));
        Gson gson = new Gson();
        String jsonToSend = gson.toJson(usersToConnect);
        // to do
        // will return json
        return jsonToSend;
    }
}
