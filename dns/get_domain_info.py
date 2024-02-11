import dns
import dns.resolver
import dns.query
import dns.zone

FQDN = "www.google.com"

ansA,ansMX,ansNS,ansAAAA=(dns.resolver.query(FQDN, "A"),
                          dns.resolver.query(FQDN, "MX"),
                          dns.resolver.query(FQDN, "NS"),
                          dns.resolver.query(FQDN, "AAAA"))

print ansA.response.to_text()
print ansMX.response.to_text()
print ansNS.response.to_text()
print ansAAAA.response.to_text()

zone = dns.zone.from_xfr(dns.query.xfr("173.194.34.192", "thehackerway.com"))
