#!/usr/bin/env python3
import socket
import os
import sys
import signal
import re

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
        f=connected_socket.makefile(mode='rw',encoding='utf-8')
        f.write('SUMATOR 1.0\n')
        f.flush()
        f.readline() # Zatial ignorujeme
        n=0
        while True:
            data=f.readline()
            print('data prijate:',data)
            if not data:
                break
            m=re.match('CISLO ([^ ]*)\n',data)
            if m:
                status_num,status_comment=(100,'OK')
                content_reply=''
                try:
                    n=n+int(m.group(1))
                except ValueError:
                    status_num,status_comment=(200,'Bad number')
            elif data=='SUMA\n':
                status_num,status_comment=(100,'OK')
                content_reply=f'{n}\n'
            else:
                status_num,status_comment=(201,'Bad request')
                content_reply=''
            f.write(f'{status_num} {status_comment}\n')
            f.write(content_reply)
            f.write('\n')
            f.flush()
        print(f'{address} uzavrel spojenie')
        sys.exit(0)
    else:
        connected_socket.close()
