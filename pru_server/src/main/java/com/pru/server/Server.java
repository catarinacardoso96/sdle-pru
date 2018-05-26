package com.pru.server;

import com.pru.data.Catalog;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.channels.AsynchronousChannelGroup;
import java.nio.channels.AsynchronousServerSocketChannel;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Server {
    private static final int THREADS = 4;

    public static void main(String[] args) {

        AsynchronousChannelGroup group;
        AsynchronousServerSocketChannel srv;
        InetSocketAddress addr;
        String host = "localhost";
        int portNumber = Integer.parseInt(args[0]);
        Catalog catalog = new Catalog();

        try {
            group = AsynchronousChannelGroup
                    .withFixedThreadPool(THREADS,
                    Executors.defaultThreadFactory());
            srv  = AsynchronousServerSocketChannel.open(group);
            addr = new InetSocketAddress(host, portNumber);
            srv.bind(addr);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        srv.accept(catalog, new CompletionHandler<AsynchronousSocketChannel, Catalog>() {

            @Override
            public void completed(AsynchronousSocketChannel res, Catalog catalog) {
                RequestProcessor rp = new RequestProcessor(res, catalog);
                rp.processAndReply();
                srv.accept(catalog, this);
            }

            @Override
            public void failed(Throwable exc, Catalog att) {
                System.exit(1);
            }
        });

        try {
            group.awaitTermination(Long.MAX_VALUE, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            System.out.println("Interrupted");
            return;
        }

    }
}
