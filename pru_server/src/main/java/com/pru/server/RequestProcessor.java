package com.pru.server;

import com.pru.data.Catalog;
import com.pru.util.PeerAnswer;

import java.nio.channels.AsynchronousSocketChannel;
import java.util.concurrent.atomic.AtomicBoolean;

public class RequestProcessor {
    private HandleReadWrite channel;
    private Catalog catalog;

    public RequestProcessor(AsynchronousSocketChannel socketChannel, Catalog catalog) {
        this.channel = new HandleReadWrite(socketChannel);
        this.catalog = catalog;
    }

    public void processAndReply() {
        this.channel.read()
                .thenApply((s) -> {
                    System.out.println(s);
                    PeerAnswer p  =catalog.update(s);
                    return p;
                })
                .thenAccept((b) -> {
                    if(b.isAnswer()){
                        this.channel.write(catalog.onlineUser(b.getHash()));
                    }
                });

    }
}
