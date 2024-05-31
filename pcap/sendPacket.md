**Creating and sending packets**

This example does a couple of things. First, it will show you how to use the network device to send raw bytes, so you can use it almost like a serial connection to send data. This is useful for really low-level data transfer, but if you want to interact with an application, you probably want to build a packet that other hardware and software can recognize.

The next thing it does is show you how to create a packet with the Ethernet, IP, and TCP layers. Everything is default and empty, though, so it doesn't really do anything.

Finally, we will create another packet, but we'll actually fill in some MAC addresses for the Ethernet layer, some IP addresses for IPv4, and port numbers for the TCP layer. You should see how you can forge packets and impersonate devices with that.

The TCP layer struct has Boolean fields for the SYN, FIN, and ACK flags, which can be read or set. This is good for manipulating and fuzzing TCP handshakes, sessions, and port scanning.

The pcap library provides an easy way to send bytes, but the layers package in gopacket assists us in creating the byte structure for the several layers.
