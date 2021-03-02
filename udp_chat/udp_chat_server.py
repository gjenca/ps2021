#!/usr/bin/env python3
import socket
import re

bind_addr=("",9999)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(bind_addr)

clients={}

while True:

    data_b,client_addr=s.recvfrom(1024)
    try:
        data=data_b.decode("utf-8")
    except UnicodeDecodeError:
        continue
    data=data.rstrip() # zmazeme biele znaky napravo
    m=re.match("^(?P<request>[^:]*):(?P<param>.*)$",data)
    if not m:
        continue
    request=m.group("request")
    param=m.group("param")
    print(client_addr,request,param)
    if request=="HELLO":
        if not param.isalnum():
            continue
        clients[client_addr]=param
    elif request=="ISAY":
        if client_addr in clients:
            nick=clients[client_addr]
            for other_addr in clients:
                if other_addr!=client_addr:
                    msg="SAYS:%s>%s" % (nick,param)
                    s.sendto(msg.encode("utf-8"),other_addr)



