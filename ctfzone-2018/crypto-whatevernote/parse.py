data = open("example.1").read().strip().split("\n")

import socket
import binascii
import sys

def sendall(sock, s):
    while len(s) != 0:
        n = sock.send(s)
        s = s[n:]

if sys.argv[1] == "server":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("127.0.0.1", 4445))
    sock.listen(5)

    (clientsock, addr) = sock.accept()

    waiting_on_them = True
    for i, c in enumerate(data):
        if waiting_on_them:
            clientsock.recv(1024)
        else:
            sendall(clientsock, binascii.unhexlify(c))

        waiting_on_them = not waiting_on_them

else:
    sock = socket.create_connection(("127.0.0.1", 4445))

    waiting_on_them = False
    for i, c in enumerate(data):
        if waiting_on_them:
            sock.recv(1024)
        else:
            sendall(sock, binascii.unhexlify(c))

        waiting_on_them = not waiting_on_them

