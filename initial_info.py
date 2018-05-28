import socket
from hashlib import md5
from netifaces import interfaces, ifaddresses, AF_INET

from fcntl import ioctl
from struct import pack, unpack
from array import array

#----------------------------------------------------------------------------------#
def hash_email(login_flag, in_email):
    if login_flag:
        #email = input('Insert email: ')
        email = in_email
    #else:
        #email = get email from DB
    print('Your email: %s' % (email))

    # md5, sha1, sha224, sha256, sha384, sha512
    hash_object = md5(email.encode())

    hash_string = hash_object.hexdigest()
    print('Your hash: %s' % (hash_string))
    return hash_string

#----------------------------------------------------------------------------------#
def get_ip(option):
    '''
    if option == 'wl':
        if ifaddresses('wlp2s0'):
            ip = ifaddresses('wlp2s0')[AF_INET][0]['addr']
        elif ifaddresses('wlp3s0'):
            ip = ifaddresses('wlp3s0')[AF_INET][0]['addr']

    elif option == 'en':
        if ifaddresses('enp2s0'):
            ip = ifaddresses('enp2s0')[AF_INET][0]['addr']
        elif ifaddresses('enp3s0'):
            ip = ifaddresses('enp3s0')[AF_INET][0]['addr']
    '''
    for f in interfaces():
        if f.startswith(option):
            ip = ifaddresses(f)[AF_INET][0]['addr']

    print('Your ip: %s' % (ip))
    return ip
'''
#----------------------------------------------------------------------------------#
def get_ip2(sock):

    #---------------------------------------------------------#
    def all_interfaces(sock):
        max_possible = 128  # arbitrary. raise if needed.
        nbytes = max_possible * 32
        
        names = array("B", b'\0' * nbytes) 
        
        outbytes = unpack('iL', ioctl(
            sock.fileno(), 0x8912, #SIOCGIFCONF
            pack('iL', nbytes, names.buffer_info()[0])
        ))[0]

        namestr = names.tostring()
        lst = []

        for i in range(0, outbytes, 40):
            name = namestr[i:i+16].split(b'\0', 1)[0]
            ip   = namestr[i+20:i+24]
            lst.append((name, ip))

        return lst

    #---------------------------------------------------------#
    def format_ip(addr):
        return str(addr[0]) + '.' + str(addr[1]) + '.' + \
               str(addr[2]) + '.' + str(addr[3])

    #---------------------------------------------------------#
    ifs = all_interfaces(sock)

    for i in ifs:
        print("%12s   %s" % (i[0].decode(), format_ip(i[1])))
'''
#----------------------------------------------------------------------------------#
def first_login():
    # check if this login is the 1st
    return True
