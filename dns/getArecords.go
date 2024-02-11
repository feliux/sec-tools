package main

import (
	"log"

	"github.com/miekg/dns"
)

var (
	domain     string = "bbva.com"
	dnsToQuery string = "8.8.8.8:53"
)

func main() {
	var msg dns.Msg
	fqdn := dns.Fqdn(domain)
	msg.SetQuestion(fqdn, dns.TypeA)
	in, err := dns.Exchange(&msg, dnsToQuery)
	if err != nil {
		panic(err)
	}
	if len(in.Answer) < 1 {
		log.Println("No records.")
		return
	}
	for _, answer := range in.Answer {
		if a, ok := answer.(*dns.A); ok {
			log.Printf("A record for domain %s: %s", domain, a.A)
		}
	}
}
