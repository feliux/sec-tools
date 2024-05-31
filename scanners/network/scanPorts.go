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
	maxPort  = 1024
)

func main() {
	activeThreads := 0
	done := make(chan bool)

	for port := minPort; port <= maxPort; port++ {
		go testTcpConnection(ipToScan, port, done)
		activeThreads++
	}

	// Wait for all threads to finish
	for activeThreads > 0 {
		<-done
		activeThreads--
	}
}

func testTcpConnection(ip string, port int, done chan bool) {
	_, err := net.DialTimeout(
		"tcp",
		ip+":"+strconv.Itoa(port),
		time.Second*10,
	)
	if err == nil {
		log.Printf("port %d: open\n", port)
	}
	done <- true
}
