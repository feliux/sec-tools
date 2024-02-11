import nmap


class NmapHost:
    def __init__(self):
        self.host = None
        self.state = None
        self.reason = None
        self.openPorts = []
        self.closedFilteredPorts = []

class NmapPort:
    def __init__(self):
        self.id = None
        self.state = None
        self.reason = None
        self.port = None
        self.name = None
        self.version = None
        self.scriptOutput = None
 
def parseNmapScan(scan):
    nmapHosts = []
    for host in scan.all_hosts():
        nmapHost = NmapHost()
        nmapHost.host = host
        if scan[host].has_key("status"):
            nmapHost.state = scan[host]["status"]["state"]
            nmapHost.reason = scan[host]["status"]["reason"]
            for protocol in ["tcp", "udp", "icmp"]:
                if scan[host].has_key(protocol):
                    ports = scan[host][protocol].keys()
                    for port in ports:
                        nmapPort = NmapPort()
                        nmapPort.port = port
                        nmapPort.state = scan[host][protocol][port]["state"]
                        if scan[host][protocol][port].has_key("script"):
                            nmapPort.scriptOutput = scan[host][protocol][port]["script"]
                        if scan[host][protocol][port].has_key("reason"):
                            nmapPort.reason = scan[host][protocol][port]["reason"]
                        if scan[host][protocol][port].has_key("name"):
                            nmapPort.name = scan[host][protocol][port]["name"]
                        if scan[host][protocol][port].has_key("version"):
                            nmapPort.version = scan[host][protocol][port]["version"]
                        if "open" in (scan[host][protocol][port]["state"]):
                            nmapHost.openPorts.append(nmapPort)
                        else:
                            nmapHost.closedFilteredPorts.append(nmapPort)
                    nmapHosts.append(nmapHost)
        else:
            print("[-] There"s no match in the Nmap scan with the specified protocol ", protocol)
    return nmapHosts
 
if __name__ == "__main__":
    import pprint
    nm = nmap.PortScanner()
    nm.scan("127.0.0.1", "22-8080", arguments="-sV -n -A -T5")
    structureNmap = parseNmapScan(nm)
    for host in structureNmap:
        print "Host: "+ host.host
        print "State: "+ host.state
        for openPort in host.openPorts:
            print str(openPort.port)+" - "+openPort.state
