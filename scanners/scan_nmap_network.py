# pip install ipcalc python-nmap

import nmap
from ipcalc import IP, Network

CIDR = "192.168.1.1/24"

my_scan = nmap.ports_to_scancanner()
ports_to_scan = (
    "21", 
    "22", 
    "25", 
    "53", 
    "80"
)

arguments = "-sS -sV -O"

def NmapScan(host, ports_to_scan):
    for port in ports_to_scan:
        try:
            my_scan.scan(
                host, 
                port, 
                arguments
            )
            if my_scan[host]["tcp"][int(port)]["state"] == "open":
                print("Host: %s , Puerto: %s, abierto" %(host, port))
        except KeyError:
            pass


if __name__ == "__main__":
    import sys
    try:
        for x in Network(CIDR):
            host = str(x)
            NmapScan(host, ports_to_scan)
    except KeyboardInterrupt:
        sys.exit()
