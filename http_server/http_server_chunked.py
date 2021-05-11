#!/usr/bin/env python3
import socket
import os
import sys
import signal
import re

DOCUMENT_ROOT='./documents'
MIME_TYPES={
    '.html':'text/html',
    '.jpg':'image/jpeg',
    '.gif':'image/gif',
    '.png':'image/png',
    '.txt':'text/plain',
    }

def send_status(f,status_num,status_txt):

    html_reply=f'''<html>
        <body>
            <h1>{status_num} {status_txt}</h1>
        </body>
        </html>'''.encode('ASCII')
    f.write(f'HTTP/1.1 {status_num} {status_txt}\r\n'.encode('ASCII'))
    f.write('Content-type: text/html\r\n'.encode('ASCII'))
    f.write(f'Content-length: {len(html_reply)}\r\n'.encode('ASCII'))
    f.write('\r\n'.encode('ASCII'))
    f.write(html_reply)
    f.flush()

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
        f=connected_socket.makefile('rwb')
        while True:
            request=f.readline().decode('ASCII')
            if not request:
                # spojenie ukoncene
                break
            print(request)
            m=re.match('^GET ([^ ]+) .*$',request)
            if not m:
                send_status(f,400,'Bad request')
                break
            # Preskocime vsetky hlavicky, ignorujeme
            for line_b in f:
                line=line_b.decode('ASCII').strip()
                if line=='':
                    break
            URL=m.group(1)
            filename=DOCUMENT_ROOT+URL
            try:
                fr=open(filename,'rb')
            except FileNotFoundError:
                send_status(f,404,'Not found')
                break
            URL_lower=URL.lower()
            for suff in MIME_TYPES:
                if URL_lower.endswith(suff):
                    mime_type=MIME_TYPES[suff]
                    break
            else:
                mime_type='application/octet-stream'
            f.write('HTTP/1.1 200 OK\r\n'.encode('ASCII'))
            f.write(f'Content-type: {mime_type}\r\n'.encode('ASCII'))
            f.write(f'Transfer-encoding: chunked\r\n'.encode('ASCII'))
            f.write('\r\n'.encode('ASCII'))
            while True:
                data=fr.read(100)
                f.write(('%x\r\n' % len(data)).encode('ASCII'))
                f.write(data)
                f.write('\r\n'.encode('ASCII'))
                if not data:
                    break
                f.flush()
            fr.close()
            f.flush()
        f.close()
        sys.exit(0)
    else:
        connected_socket.close()
