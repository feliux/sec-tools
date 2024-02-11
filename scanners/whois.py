import pythonwhois
import sys

if len(sys.argv) != 2:
    print("[-] usage python B1-01.py <domain_name>")
    sys.exit()

whois = pythonwhois.get_whois(sys.argv[1])
for key in whois.keys():
    print("[+] %s : %s \n" %(key, whois[key]))