package com.pru.server;

import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;
import java.util.concurrent.CompletableFuture;

public class HandleReadWrite {

    private ByteBuffer buf, line;
    private AsynchronousSocketChannel sock;

    public HandleReadWrite(AsynchronousSocketChannel sock) {
        this.sock = sock;
        this.buf  = ByteBuffer.allocate(1024);
        this.line = ByteBuffer.allocate(1024);
    }

    public CompletableFuture<String> read() {
        return read(new CompletableFuture<>());
    }

    private CompletableFuture<String> read(CompletableFuture<String> r) {
        buf.flip();
        while(buf.hasRemaining()) {
            byte c = buf.get();
            System.out.print((char)c);
            if (c == '\n') {
                line.flip();
                byte b[] = new byte[line.remaining()];
                line.get(b);
                String res = new String(b);
                line.clear();
                buf.clear();
                r.complete(res);
                return r;
            } else {
                line.put(c);
            }
        }

        buf.clear();

        sock.read(buf, null, new CompletionHandler<Integer, Object>() {

            @Override
            public void completed(Integer result, Object attachment) {

            }

            @Override
            public void failed(Throwable exc, Object attachment) {

            }
        });

        return r;
    }

    public CompletableFuture<String> write(String s) {
        CompletableFuture<String> cf = new CompletableFuture<>();
        sock.write(ByteBuffer.wrap(s.getBytes()),
                null,
                new CompletionHandler<Integer, Object>() {
                    @Override
                    public void completed(Integer result, Object attachment) {
                        cf.complete(s);
                    }

                    @Override
                    public void failed(Throwable exc, Object attachment) {

                    }
                });
        return cf;
    }

}