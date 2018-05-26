package com.pru.server;

import com.pru.data.Catalog;

import java.nio.channels.AsynchronousSocketChannel;

public class RequestProcessor {
    private AsynchronousSocketChannel socketChannel;
    private Catalog catalog;

    public RequestProcessor(AsynchronousSocketChannel socketChannel, Catalog catalog) {
        this.socketChannel = socketChannel;
        this.catalog = catalog;
    }

    public void processAndReply() {

    }
}
