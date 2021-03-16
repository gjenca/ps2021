#!/usr/bin/env python3
import socket
import os
import sys
import signal

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',9999))
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
s.listen(5)

while True:
    connected_socket,address=s.accept()
    print(f'spojenie z {address}')
    pid_chld=os.fork()
    if pid_chld==0:
        s.close()
        while True:
            bs=connected_socket.recv(1024)
            print('data prijate')
            if not bs:
                break
            connected_socket.send(b'PONG\n')
        print(f'{address} uzavrel spojenie')
        sys.exit(0)
    else:
        connected_socket.close()
