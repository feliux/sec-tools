
```sh
#scapy //Con esto entramos en el interprete de scapy y podemos comenzar a utilizar sus funciones.
scapy>ls() //Con la función ls() podemos ver los protocolos soportados por scapy.
scapy>lsc() //Con lsc() vemos las funciones disponibles en scapy
scapy>packet = Ether()/IP(dst="google.com")/ICMP()/"ABCD" //Aquí hemos creado un paquete del tipo ICMP y como se puede ver es necesario declarar cada una de las capas que componen el paquete. En este caso, necesitamos una capa Ethernet, IP, ICMP y finalmente los datos raw de aplicación.
scapy>ls(packet) #Con ls() tambien podemos enseñar la estructura de un paquete determinado. Como se puede apreciar, incluye la información de cada una de las capas del paquete.
scapy>sendp(packet) #Con la funcion sendp enviamos el paquete a su correspondiente destino.
scapy>sendp(paquet, loop=1, inter=1) #Con las opciones inter y loop podemos enviar el paquete de forma indefinida cada N segundos.
scapy> srp1(packet) #Si lo que queremos es enviar y recibir paquetes, la función srp1 puede sernos util.
scapy> _.show() 
scapy> _.summary() #Con estas funciones, vemos el paquete recibido en un formato mucho más amigable y simplificado.
scapy> pkts = sniff(iface="wlan0", count=3) #Con la función sniff podemos capturar paquetes del mismo modo que lo hacen herramientas como tcpdump o wireshark
scapy> pkts[0] 
scapy> pkts[1] 
scapy> pkts[2]
scapy> wrpcap("demo.pcap", pkts) #Si queremos almacenar un conjunto de paquetes en un fichero PCAP, podemos utilizar la funcion wrpcap.
scapy> readed = rdpcap("demo.pcap") #Con la función rdpcap podemos leer un fichero pcap y obtener un listado de paquetes que pueden ser manejados desde python.
scapy> readed[0]
scapy> readed[1]

Scapy soporta el formato BPF (Berkeley Packet Filters) el cual es un formato estandar para aplicar filtros sobre paquetes de red. Estos filtros pueden aplicarse sobre un conjunto de paquetes o directamente sobre una captura activa.

scapy> icmpPkts = sniff(iface="wlan0", filter="icmp" count=3) #Aquí filtramos por los paquetes del tipo ICMP.

ping www.google.com

scapy> icmpPkts[0]
scapy> icmpPkts[1]
scapy> icmpPkts[2]
scapy> sniff(iface="eth0", count=3, prn=lambda x: x.summary()) #Otra caracteristica interesante de la función sniff, es que cuenta con el atributo "prn" el cual permite ejecutar una función cuando se captura un paquete. Se trata de algo muy util si queremos manipular y reinyectar paquetes de datos.

scapy> conf #Desde el interprete, tenemos acceso al comando conf, el cual nos permite ver y editar la configuración con la que trabaja Scapy.
scapy> conf.route
scapy> conf.route.add[net="192.168.2.0/24", gw="192.168.2.1"]
scapy> conf.route
scapy> conf.route.resync()
scapy> conf.route #En este caso hemos manipulado la tabla de ruteo que tiene scapy internamente.
```
