from ui import *
from initial_info import *
from timeline import *

import sys
import threading

#----------------------------------------------------------------------------------#
class Peer():

    #---------------------------------------------------------#
    def __init__(self):
        self.server = ("localhost", 8080)

        self.login_flag = first_login()
        self.e_hash = hash_email(self.login_flag)
        self.ip = get_ip()
        self.sock = self.connect_server()
        #self.ip2 = get_ip2(self.sock)

        # send hash and ip to server
        self.initial_commit()

        self.user = User(self.login_flag)
        self.background_app(int(sys.argv[1]))
        self.foreground_app()

    #---------------------------------------------------------#
    def connect_server(self):
        # AF_UNIX - same machine; AF_INET - IPv4; AF_INET6 - IPv6
        # TCP - SOCK_STREAM; UDP - SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server)
        return sock

    #---------------------------------------------------------#
    def send_to_server(self, msg):
        self.sock.send((msg+"\n").encode())

    #---------------------------------------------------------#
    def recv_msg(self, sock):
        data = sock.recv(1024).decode()
        print('Message: %s' % (data))
        return data

    #---------------------------------------------------------#
    def initial_commit(self):
        self.send_to_server(self.e_hash)
        self.send_to_server(self.ip)

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

        self.user.save()
        print_pigeon()
        sys.exit()

#----------------------------------------------------------------------------------#
def main():
    print_pigeon()
    peer = Peer()
    
if __name__ == "__main__":
    main()
