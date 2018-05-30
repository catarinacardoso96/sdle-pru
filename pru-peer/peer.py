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

        #self.server = ("10.0.0.2", 11111)
        #self.server = ("localhost", 8080)
        self.server = ("192.168.1.125", 11111)

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
        #print('Message: %s' % (data))
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
            #print("wait for message")
            data = self.recv_msg(client_sock)
            if not data:
                break

            json_data = json.loads(data)

            peers_to_send = self.peers.copy()
            for key, sock in peers_to_send.items():
                if sock == client_sock:
                    del peers_to_send[key]
                    break

            if json_data['ttl'] == 0:
                continue
            else:
                json_data['ttl'] -= 1

            data = json.dumps(json_data)

            if json_data["type"] == "post":
                relevant_posts = self.select_posts(json_data['content'], self.user.following)
                self.user.others_posts += relevant_posts
                self.update_following(relevant_posts)
                for p in peers_to_send.values():
                    self.fload_post(p, data)

            elif json_data["type"] == "req":
                relevant_posts =  self.select_posts( self.get_posts(), json_data['content'])
                ip, port = json_data['addr']
                if relevant_posts:
                    j_str = json.dumps({'type' : 'post', 'ttl' : 1 , 'content' : relevant_posts})
                    if (ip, port) in self.peers :
                        sock = self.peers[(ip,port)]
                        sock.send(j_str.encode())
                    else:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((ip, port))
                        sock.send(j_str.encode())
                        if len(self.peers) < 10:
                            self.peers[(ip, port)] = sock
                        else:
                            sock.close()

                for p in peers_to_send.values():
                    self.fload_post(p, data)

            elif json_data["type"] == "conn":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip, port = json_data['addr']
                sock.connect((ip, port))
                self.handshake_connect(sock)

        client_sock.close()

    #---------------------------------------------------------#
    def update_following(self, relevant_posts):
        for post in relevant_posts:
            email = post['from']
            id_post = post['id']
            if email in self.user.following:
                if self.user.following[email] < id_post:
                    self.user.following[email] = id_post

    #---------------------------------------------------------#
    def select_posts(self, posts, peer_following):
        posts_send = []
        for p in posts:
            email = p['from']
            id_post = p['id']
            if email in peer_following:
                if peer_following[email] < id_post:
                    posts_send.append(p)

        return posts_send

    #-----------------------------------------------------#
    def handshake_connect(self, sock, peer):
        #envia ip
        j_str = json.dumps({"ip": self.ip, "port": self.port})
        sock.send((j_str).encode())
        self.peers[(peer['ip'], peer['port'])] = sock

        #recebe following
        peer_following = self.recv_msg(sock)
        all_posts = self.get_posts()

        #envia following
        following = self.user.following
        j_str = json.dumps(following)
        sock.send((j_str).encode())

        #recebe posts
        posts_from_peer = self.recv_msg(sock)
        self.user.others_posts += json.loads(posts_from_peer)

        #select and send posts
        posts_to_send = self.select_posts(all_posts, json.loads(peer_following))
        j_str = json.dumps(posts_to_send)
        sock.send((j_str).encode())

    #---------------------------------------------------------#
    def connect_with_peer(self, peer):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer['ip'], peer['port']))

        self.handshake_connect(sock, peer)

        thread = threading.Thread(target=self.handle_peer, args=(sock,))
        thread.daemon = True
        thread.start()

    #-----------------------------------------------------#
    def handshake_accept(self, client_sock, flag):
        #recebe ip
        msg = self.recv_msg(client_sock)
        j_str = json.loads(msg)
        if flag:
            self.peers[(j_str['ip'], j_str['port'])] = client_sock
        else:
            j_str = json.dumps({'type': 'conn', 'ttl': 1, 'addr': (j_str['ip'], j_str['port'])})
            key, value = self.peers.items()[-1]
            value.send(j_str.encode())

        #envia following
        following = self.user.following
        j_str = json.dumps(following)
        client_sock.send((j_str).encode())

        #recebe following
        peer_following = self.recv_msg(client_sock)
        all_posts = self.get_posts()

        #select and send posts
        posts_to_send = self.select_posts(all_posts, json.loads(peer_following))
        j_str = json.dumps(posts_to_send)
        client_sock.send((j_str).encode())

        #recebe posts
        posts_from_peer = self.recv_msg(client_sock)
        self.user.others_posts += json.loads(posts_from_peer)

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
                #print("listening on: " + self.ip + ":" + str(self.port))
                client_sock, _ = sock.accept()

                if len(self.peers) > 10:
                    # sugest another socket to new client
                    self.handshake_accept(client_sock, False)
                    client_sock.close()
                else:
                    self.handshake_accept(client_sock, True)

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
    def fload_post(self, sock, post):
        
        sock.send((post).encode())
        
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
                j_str = json.dumps({'type' : 'post', 'ttl' : 6, 'content' : [post]})
                for p in self.peers.values():
                    self.fload_post(p, j_str)

            elif option == 2:
                j_str = json.dumps({'type' : 'req', 'ttl' : 6, 'addr' : (self.ip, self.port), 'content' : self.user.following})
                for p in self.peers.values():    
                    self.fload_post(p, j_str)

            elif option == 3:
                print_timeline(self.user.others_posts)

            elif option == 4:
                print_timeline(self.user.my_posts)

            elif option == 5:
                self.user.follow()

            elif option == 6:
                self.user.unfollow()

        self.final_commit()
        self.user.save()
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
