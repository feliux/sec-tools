package main

import "github.com/miekg/dns"

var (
	domain     string = "bbva.com"
	dnsToQuery string = "8.8.8.8:53"
)

func main() {
	var msg dns.Msg
	fqdn := dns.Fqdn(domain)
	msg.SetQuestion(fqdn, dns.TypeA)
	dns.Exchange(&msg, dnsToQuery) // sudo tcpdump -i eth0 -n udp port 53
}
