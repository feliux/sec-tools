# -*- encoding: utf-8 -*-

import logging
from scapy.all import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

if len(sys.argv) != 3:
    print("usage: python window_scan.py <ip address> <list of ports separated by colon>")
    exit()

src_port = RandShort()
dst_ip = sys.argv[1]
ports = sys.argv[2]
ports.replace(" ", "")
scanPorts = ports.strip().split(':')

for port in scanPorts:
    response = sr1(IP(dst=dst_ip)/TCP(dport=int(port),flags="A"), timeout=5)
    if (str(type(response))=="<type 'NoneType'>"):
        print("Sin respuesta")
    elif(response.haslayer(TCP)):
        if(response.getlayer(TCP).window == 0):
            print("Closed")
        elif(response.getlayer(TCP).window > 0):
            print("Open")
