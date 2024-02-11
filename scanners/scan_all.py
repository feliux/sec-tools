import argparse
import json
import whois
import dns.resolver
import nmap3
import shodan
import requests

_CHOICES = ["true", "false"]
nmap_ports = []
shodan_ports = []
parser = argparse.ArgumentParser(
    prog="scan_all.py",
    description="Extract domain data.",
    usage="python %(prog)s [-d/--domain -w/--whois --dns -n/--nmap --shodan-key]"
)
parser.add_argument("-d", "--domain", required=True, type=str, help="Domain name to query.")
parser.add_argument("-w", "--whois", required=True, type=str, choices=_CHOICES, help="Get whois data. Values: true or false.")
parser.add_argument("--dns", required=True, type=str, choices=_CHOICES, help="Get DNS data. Values: true or false.")
parser.add_argument("-n", "--nmap", required=True, type=str, choices=_CHOICES, help="Scan using nmap. Values: true or false.")
parser.add_argument("--shodan-key", required=False, type=str, help="Shodan API key.")
_SCRIPT_ARGUMENTS = parser.parse_args()

# WHOIS
if _SCRIPT_ARGUMENTS.whois == "true":
    try:
        w = whois.whois(_SCRIPT_ARGUMENTS.domain)
        print(f"[+] Wois data:\n {w}")
    except Exception as e:
        print(e)

# DNS https://support.google.com/a/answer/48090?hl=es-419
if _SCRIPT_ARGUMENTS.dns == "true":
    try:
        ansA, ansMX, ansNS, ansAAAA = (
            dns.resolver.resolve(_SCRIPT_ARGUMENTS.domain, "A"),
            dns.resolver.resolve(_SCRIPT_ARGUMENTS.domain, "MX"),
            dns.resolver.resolve(_SCRIPT_ARGUMENTS.domain, "NS"),
            dns.resolver.resolve(_SCRIPT_ARGUMENTS.domain, "AAAA")
        )
        print(f"[+] DNS A register:\n {ansA.response.to_text()}\n")
        print(f"[+] DNS MX register:\n {ansMX.response.to_text()}\n")
        print(f"[+] DNS NS register:\n {ansNS.response.to_text()}\n")
        print(f"[+] DNS AAAA register:\n {ansAAAA.response.to_text()}\n")
    except Exception as e:
        print(e)

# NMAP
if _SCRIPT_ARGUMENTS.nmap == "true":
    _NMAP_ARGS = "-p- --open -Pn -n -v --min-rate 5000"
    try:
        nmap = nmap3.NmapHostDiscovery()
        nmap_result = nmap.nmap_portscan_only(_SCRIPT_ARGUMENTS.domain, args=_NMAP_ARGS)
        ip = list(nmap_result.keys())[0]
        print(f"[+] NMAP:\n {json.dumps(nmap_result, indent=4)}")
        for port in nmap_result[ip]["ports"]:
            nmap_ports.append(port["portid"])
        nmap_ports = list(set(nmap_ports))
        print("NMAP open ports", nmap_ports)
    except Exception as e:
        print(e)
elif _SCRIPT_ARGUMENTS.nmap == "false":
    pass
else:
    raise argparse.ArgumentTypeError("Error: -n/--nmap argument must be true or false.")

# SHODAN
if _SCRIPT_ARGUMENTS.shodan_key:
    SHODAN_API_KEY = _SCRIPT_ARGUMENTS.shodan_key
    try:
        shodan = shodan.Shodan(SHODAN_API_KEY)
        shodan_result = shodan.host(ip)
        # shodan_result = shodan.search(f"hostname:{_SCRIPT_ARGUMENTS.domain}")
        print("[+] SHODAN:\n")  # {json.dumps(shodan_result, indent=4)}")
        print("IP: {}\nOrganization: {}\nOperating System: {}\n".format(
            shodan_result["ip_str"],
            shodan_result.get("org", "n/a"),
            shodan_result.get("os", "n/a"))
        )
        for item in shodan_result["data"]:
            print("Port: {}\nBanner: {}".format(item["port"], item["data"]))
            shodan_ports.append(str(item["port"]))
        shodan_ports = list(set(shodan_ports))
    except Exception as e:
        print(e)

print("[+] REQUEST for HTTP/HTTPs:\n")
total_ports = list(set(nmap_ports + shodan_ports))
for port in total_ports:
    if port == "80" or port == "8080":
        try:
            result = requests.get(f"http://{_SCRIPT_ARGUMENTS.domain}")
            print(f"Response for HTTP port {port}: {result.status_code}")
        except Exception:
            print(f"No response for HTTP port {port}.")
            pass
    elif port == "443":
        try:
            result = requests.get(f"https://{_SCRIPT_ARGUMENTS.domain}")
            print("Response for HTTPs:\n", result.status_code)
        except Exception:
            print("No response for HTTPs.")
