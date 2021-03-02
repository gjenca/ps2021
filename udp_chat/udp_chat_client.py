#!/usr/bin/env python3
import socket
import os
import sys

addr_server=(sys.argv[1],9999)
nick=sys.argv[2]
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

greeting="HELLO:%s" % nick
s.sendto(greeting.encode("utf-8"),addr_server)

if os.fork():

    while True:
        data_b,odkial=s.recvfrom(1024)
        if odkial!=addr_server:
            continue
        data=data_b.decode("utf-8")
        if not data.startswith("SAYS:"):
            continue
        sys.stdout.write(data[5:].rstrip())
        sys.stdout.write('\n')
else:
    while True:
        line=sys.stdin.readline()
        message="ISAY:%s" % line
        s.sendto(message.encode("utf-8"),addr_server)



