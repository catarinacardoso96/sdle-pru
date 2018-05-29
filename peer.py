from ui import *
from initial_info import *
from timeline import *

from sys import argv, exit
import socket
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
            self.user.email = email
        else:
            email = self.user.email

        self.server = ("10.0.0.2", 11111)
        #self.server = ("localhost", 8080)
        
        self.e_hash = hash_email(email)
        self.ip = get_ip(argv[2])
        self.port = int(argv[1])
        
        self.peers = {}
        self.sockets = []
        self.initial_commit()

        self.background_app()
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
        peers = json.loads(peers)

        for p in peers:
            self.connect_with_peer(p)

    #---------------------------------------------------------#
    def final_commit(self):
        j_str = json.dumps({"hash": self.e_hash})
        sock = self.send_to_server(j_str)
        self.disconnect_from_server(sock)

    #---------------------------------------------------------#
    def handle_peer(self, client_sock):
        while True:
            print("wait for message")
            data = self.recv_msg(client_sock)
            self.send_posts(client_sock, self.get_posts(), data)
            if not data:
                break
        client_sock.close()

    #---------------------------------------------------------#
    def connect_with_peer(self, peer):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer['ip'], peer['port']))

        j_str = json.dumps({"ip": self.ip, "port": self.port})
        sock.send((j_str).encode())
        
        self.peers[(peer['ip'], peer['port'])] = sock

        thread = threading.Thread(target=self.handle_peer, args=(sock,))
        thread.daemon = True
        thread.start()

    #---------------------------------------------------------#
    def background_app(self):

        #-----------------------------------------------------#
        def accept_peers():
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.ip, self.port))
            sock.listen(5)
            # argument specifies the maximum number of queued connections and
            # should be at least 0, the maximum value is system-dependent (usually 5)

            while True:
                print("listening on: " + self.ip + ":" + str(self.port))
                client_sock, _ = sock.accept()
                msg = self.recv_msg(client_sock)
                j_str = json.loads(msg)
                self.peers[(j_str['ip'], j_str['port'])] = client_sock

                thread = threading.Thread(target=self.handle_peer, args=(client_sock,))
                thread.daemon = True
                thread.start()
            sock.close()

        thread = threading.Thread(target=accept_peers)
        thread.daemon = True
        thread.start()

    #---------------------------------------------------------#
    def get_posts(self):
        return self.user.my_posts + self.user.others_posts

    #---------------------------------------------------------#
    def send_posts(self, sock, posts, previous_posts):
        #posts lista
        if not previous_posts:
            j_str = json.dumps(posts)
            sock.send((j_str+"\n").encode())
        else:
            for pp in previous_posts:
                if pp in posts:
                    posts.remove(pp)
            j_str = json.dumps(posts)
            sock.send((j_str+"\n").encode())

    #---------------------------------------------------------#
    '''
    def send_to_peer(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 7070))
        msg = make_post()
        sock.sendto((msg+"\n").encode(), ("localhost", 7070)) 
    '''

    #---------------------------------------------------------#
    def close_peers(self):
        for p in self.peers.values():
            p.close()

    #---------------------------------------------------------#
    def foreground_app(self):
        option = -1
        while option != 0:
            option = select_action()

            if option == 1:
                post = self.user.make_post()
                for p in self.peers.values():
                    self.send_posts(p, [post], None)

            elif option == 2:
                followers = self.user.followers
                # fetch new posts from followers
                #print_timeline()

            elif option == 3:
                print_timeline(self.user.my_posts)

            elif option == 4:
                answer, email = self.user.follow()
                if answer:
                    print()
                    # fetch new posts from email

            elif option == 5:
                self.user.unfollow()

        self.final_commit()
        #self.user.save()
        self.close_peers()
        print_pigeon()

#----------------------------------------------------------------------------------#
def main():
    if len(argv) < 4:
        print("Wrong input!\npython file.py port interface email")

    print_pigeon()

    peer = Peer()
    
if __name__ == "__main__":
    main()
