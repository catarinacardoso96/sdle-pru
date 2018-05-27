package com.pru.server;

import com.pru.data.Catalog;
import com.pru.data.Entry;

import java.nio.channels.AsynchronousSocketChannel;

public class RequestProcessor {
    private HandleReadWrite channel;
    private Catalog catalog;

    public RequestProcessor(AsynchronousSocketChannel socketChannel, Catalog catalog) {
        this.channel = new HandleReadWrite(socketChannel);
        this.catalog = catalog;
    }

    public void processAndReply() {
        Entry entry = new Entry();
        this.channel.read()
                .thenAccept((s) -> entry.updateEntry(s))//update de mais um user online?
                .thenRun(() -> {
                    this.channel.write(catalog.onlineUser());
                });

    }
}
