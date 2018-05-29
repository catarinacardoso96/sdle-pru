import java.io.*;
import java.net.*;
 
class TinyServer {
    public static void main(String args[]) throws Exception {
        String fromClient;
        String toClient;
 
        ServerSocket server = new ServerSocket(8080); 
        boolean run = true;
        
        while(run) {

            Socket client = server.accept();
            System.out.println("got connection on port 8080");

            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            PrintWriter out = new PrintWriter(client.getOutputStream(),true);
            
            fromClient = in.readLine();
            System.out.println("received: " + fromClient);
        
            System.out.println("sent hello");
            out.println("[{\"ip\":\"123\",\"port\":78},{\"ip\":\"456\",\"port\":90}]");

        }
        System.exit(0);
    }
}
