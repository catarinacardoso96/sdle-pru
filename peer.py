from ui import *
from initial_info import *
from timeline import *

from sys import argv, exit
import threading
import json

#----------------------------------------------------------------------------------#
class Peer():

    #---------------------------------------------------------#
    def __init__(self):
        self.user = User()
        login_flag = self.user.login_flag

        if (login_flag):
            email = argv[3]
        else:
            email = self.user.email

        #self.server = ("10.0.0.2", 11111)
        self.server = ("localhost", 8080)
        
        self.e_hash = hash_email(email)
        self.ip = get_ip(argv[2])
        self.port = int(argv[1])
        
        self.peers = []
        self.initial_commit()

        #self.background_app(self.port)
        self.foreground_app()

    #---------------------------------------------------------#
    def send_to_server(self, msg):
        # AF_UNIX - same machine; AF_INET - IPv4; AF_INET6 - IPv6
        # TCP - SOCK_STREAM; UDP - SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server)
        sock.send((msg+"\n").encode())
        return sock

    #---------------------------------------------------------#
    def recv_msg(self, sock):
        data = sock.recv(1024).decode()
        print('Message: %s' % (data))
        return data

    #---------------------------------------------------------#
    def disconnect_from_server(self, sock):
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    #---------------------------------------------------------#
    def initial_commit(self):
        j_str = json.dumps({"ip": self.ip, "port": self.port, "hash": self.e_hash})
        sock = self.send_to_server(j_str)
        peers = self.recv_msg(sock)
        self.disconnect_from_server(sock)
        self.peers = json.loads(peers) # to access: self.peers[0]['ip'] - list of dict

    #---------------------------------------------------------#
    def final_commit(self):
        j_str = json.dumps({"hash": self.e_hash})
        sock = self.send_to_server(j_str)
        self.disconnect_from_server(sock)

    #---------------------------------------------------------#
    def background_app(self, port):

        #-----------------------------------------------------#
        def accept_peers(port):

            #-------------------------------------------------#
            def handle_peer(client_sock):
                while True:
                    print("wait for message")
                    data = self.recv_msg(client_sock)
                    if not data: break
                    print('Sending: ' + data)
                    client_sock.send(data.encode())
                client_sock.close()


            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("localhost", port))
            sock.listen(5)
            # argument specifies the maximum number of queued connections and
            # should be at least 0, the maximum value is system-dependent (usually 5)
            #print("waiting for connection on port " + str(port))

            while True:
                client_sock, _ = sock.accept()
                print("got connection on port " + str(port)\
                      + " from port " + str(client_sock.getsockname()[1]))
                thread = threading.Thread(target=handle_peer, args=(client_sock,))
                thread.start()
            sock.close()

        thread = threading.Thread(target=accept_peers, args=(port,))
        thread.daemon = True
        thread.start()

    #---------------------------------------------------------#
    '''
    def send_to_peer(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 7070))
        msg = make_post()
        sock.sendto((msg+"\n").encode(), ("localhost", 7070)) 
    '''
    #---------------------------------------------------------#
    def foreground_app(self):
        option = -1
        while option != 0:
            option = select_action()

            if option == 1:
                post = self.user.make_post()
                # send post to my followers

            elif option == 2:
                followers = self.user.get_followers()
                # fetch new posts from followers
                print_timeline()

            elif option == 3:
                answer, email = self.user.follow()
                #if answer:
                    # fetch new posts from email

            elif option == 4:
                answer = self.user.unfollow()

        self.final_commit()
        self.user.save()
        print_pigeon()
        exit()

#----------------------------------------------------------------------------------#
def main():
    print_pigeon()
    if len(argv) < 4:
        print("Wrong input! port interface email")
    peer = Peer()
    
if __name__ == "__main__":
    main()
