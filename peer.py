from ui import *
from initial_info import *

#-----------------------------------------------------------------------------------------#
def connect_server(host, port):
    # AF_UNIX - same machine; AF_INET - IPv4; AF_INET6 - IPv6
    # TCP - SOCK_STREAM; UDP - SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

#-----------------------------------------------------------------------------------------#
def send_msg(socket, host, port, msg):
    sock.sendto((msg+"\n").encode('utf-8'),(host, port))

#-----------------------------------------------------------------------------------------#
def recv_msg(sock):
    data = sock.recv(1024).decode()
    print('Message: %s' % (data))

#-----------------------------------------------------------------------------------------#

host = "localhost"
port = 8080

print_pigeon()
e_hash = hash_email()
ip = get_ip()

sock = connect_server(host, port)
#get_ip2(sock)

send_msg(sock, host, port, e_hash)
send_msg(sock, host, port, ip)
recv_msg(sock)
