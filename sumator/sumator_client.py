#!/usr/bin/env python3
import socket
import sys
import re

adresa=sys.argv[1]

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((adresa,9999))
f=s.makefile(mode='rw',encoding='utf-8')
f.readline()
f.write('SUMATOR 1.0\n')
f.flush()
for line in sys.stdin:
    for word in line.split():
        print('posielam',word)
        f.write(f'CISLO {word}\n')
        f.flush()
        l=f.readline()
        print(f'Server poslal riadok\n{l}\n',file=sys.stderr)
        l=l.rstrip()
        m=re.match(r'(\d+) (.*)',l)
        if not m:
            print(f'Server poslal riadok\n{l}\n',file=sys.stderr)
            sys.exit(1)
        status_num=int(m.group(1))
        status_kom=m.group(2)
        if status_num!=100:
            print(f'Server status:{status_num} {status_kom}',file=sys.stderr)
            sys.exit(1)
        print(f'Server status:{status_num} {status_kom}',file=sys.stderr)
        f.readline()
f.write('SUMA\n')
f.flush()
f.readline() # Doplnit: kontrola statusu
print(f.readline()) # Doplnit: kontrola obsahu odpovede

