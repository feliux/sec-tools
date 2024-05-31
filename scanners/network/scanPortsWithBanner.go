package main

import (
	"log"
	"net"
	"strconv"
	"time"
)

var (
	ipToScan = "127.0.0.1"
	minPort  = 0
	maxPort  = 8080
)

func main() {
	activeThreads := 0
	done := make(chan bool)

	for port := minPort; port <= maxPort; port++ {
		go grabBanner(ipToScan, port, done)
		activeThreads++
	}

	// Wait for all threads to finish
	for activeThreads > 0 {
		<-done
		activeThreads--
	}
}

func grabBanner(ip string, port int, done chan bool) {
	connection, err := net.DialTimeout(
		"tcp",
		ip+":"+strconv.Itoa(port),
		time.Second*10,
	)
	if err != nil {
		done <- true
		return
	}
	if err == nil {
		log.Printf("port %d: open\n", port)
	}

	// See if server offers anything to read
	buffer := make([]byte, 4096)
	connection.SetReadDeadline(time.Now().Add(time.Second * 5))
	// Set timeout
	numBytesRead, err := connection.Read(buffer)
	if err != nil {
		done <- true
		return
	}
	log.Printf("banner from port %d\n%s\n", port, buffer[0:numBytesRead])
	done <- true
}
