# pip install ipcalc scapy

from ipcalc import IP, Network
from scapy.all import srp, Ether, ARP, conf

CIDR = "192.168.1.1/24"
# Deactivate verbose from packet capture and sending packets
conf.verb=0

for ip in Network(CIDR):
    # MAC broadcast. Returns MAC
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(ip)), timeout=2)
    for snd, rcv in ans:
        print(rcv.sprintf(r"%Ether.src% y %ARP.psrc%"))
