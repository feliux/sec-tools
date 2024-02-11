# -*- encoding: utf-8 -*-

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
if len(sys.argv) != 3:
    print "usage: python udp_scan.py <ip address> <list of ports separated by colon>"
    exit()
src_port = RandShort()
dst_ip = sys.argv[1]
ports = sys.argv[2]
ports.replace(" ", "")
scanPorts = ports.strip().split(':')

for port in scanPorts:
    response = sr1(IP(dst=dst_ip)/UDP(dport=int(port)),timeout=5)
    if (str(type(response))=="<type 'NoneType'>"):
        retrans = []
        for count in range(0,3):
            retrans.append(sr1(IP(dst=dst_ip)/UDP(dport=int(port)), timeout=5))
            for item in retrans:
                if (response.haslayer(UDP)):
                    print port+": Open"
                elif(response.haslayer(ICMP)):
                    if(int(response.getlayer(ICMP).type)==3 and int(response.getlayer(ICMP).code)==3):
                        print port+": Closed"
                    elif(int(response.getlayer(ICMP).type)==3 and int(response.getlayer(ICMP).code) in [1,2,9,10,13]):
                        print port+": Filtered"