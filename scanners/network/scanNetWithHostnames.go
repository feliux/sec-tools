package main

import (
	"log"
	"net"
	"strconv"
	"strings"
)

var subnetToScan = "192.168.0" // First three octets

func main() {
	activeThreads := 0
	done := make(chan bool)

	for ip := 0; ip <= 255; ip++ {
		fullIp := subnetToScan + "." + strconv.Itoa(ip)
		go resolve(fullIp, done)
		activeThreads++
	}

	// Wait for all threads to finish
	for activeThreads > 0 {
		<-done
		activeThreads--
	}
}

func resolve(ip string, done chan bool) {
	addresses, err := net.LookupAddr(ip)
	if err == nil {
		log.Printf("%s - %s\n", ip, strings.Join(addresses, ", "))
	}
	done <- true
}
