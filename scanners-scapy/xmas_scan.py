# -*- encoding: utf-8 -*-

import logging
from scapy.all import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

if len(sys.argv) != 3:
    print("usage: python xmas.py <ip address> <list of ports separated by colon>")
    exit()
    
destination = sys.argv[1]
ports = sys.argv[2]
ports.replace(" ", "")
scanPorts = ports.strip().split(':')
for port in scanPorts:
    if port.isdigit():
        response = sr1(IP(dst=destination)/TCP(dport=int(port),flags="FPU"), timeout=5)
        if response is None:
            print("[*] Puerto %s Open|Filtered " %(port))
        elif(response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14):
            print("[-] Puerto %s Closed" %(port))
        elif(response.haslayer(ICMP)) and int(response.getlayer(ICMP).type)==3:
            print("[-] Puerto %s Filtered" %(port))
        else:
            print("[-] Puerto %s invalido..." %(port))
