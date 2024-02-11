### Port Scanning Through SYN-flood Protections

**SYN cookies**

In some instances, a usual port scanner can still produce incorrect results. Specifically, when an organization employs SYN-flood protections, typically all ports (open, closed, and filtered alike) produce the same packet exchange to indicate that the port is open. These protections, known as ***SYN cookies***, prevent SYN-flood attacks and obfuscate the attack surface, producing false-positives.

When a target is using ***SYN cookies***, how can you determine whether a service is listening on a port or a device is falsely showing that the port is open? After all, in both cases, the TCP three-way handshake is completed. Most tools and scanners (Nmap included) look at this sequence (or some variation of it, based on the scan type you’ve chosen) to determine the status of the port. Therefore, you can’t rely on these tools to produce accurate results.

However, if you consider what happens after you’ve established a connection (an exchange of data, perhaps in the form of a service banner) you can deduce whether an actual service is responding. SYN-flood protections generally won’t exchange packets beyond the initial three-way handshake unless a service is listening, so the presence of any additional packets might indicate that a service exists.

**Checking TCP Flags**

To account for ***SYN cookies***, you have to extend your port-scanning capabilities to look beyond the three-way handshake by checking to see whether you receive any additional packets from the target after you’ve established a connection. You can accomplish this by sniffing the packets to see if any of them were transmitted with a TCP flag value indicative of additional, legitimate service communications.

TCP flags indicate information about the state of a packet transfer. If you look at the TCP specification, you’ll find that the flags are stored in a single byte at position 14 in the packet’s header. Each bit of this byte represents a single flag value. The flag is “on” if the bit at that position is set to 1, and “off” if the bit is set to 0.

Once you know the positions of the flags you care about, you can create a filter that checks them. For example, you can look for packets containing the following flags, which might indicate a listening service:

- ACK and FIN
- ACK
- ACK and PSH

Because you have the ability to capture and filter certain packets by using the `gopacket` library, you can build a utility that attempts to connect to a remote service, sniffs the packets, and displays only the services that communicate packets with these TCP headers. Assume all other services are falsely “open” because of SYN cookies.

**Building the BPF Filter**

Your BPF filter needs to check for the specific flag values that indicate packet transfer. The flag byte has the following values if the flags we mentioned earlier are turned on

- ACK and FIN: 00010001 (0x11)
- ACK: 00010000 (0x10)
- ACK and PSH: 00011000 (0x18)

We included the hex equivalent of the binary value for clarity, as you’ll use the hex value in your filter. To summarize, you need to check the 14th byte (offset 13 for a 0-based index) of the TCP header, filtering only for packets whose flags are 0x11, 0x10, or 0x18. Here’s what the BPF filter looks like:

~~~
tcp[13] == 0x11 or tcp[13] == 0x10 or tcp[13] == 0x18
~~~
