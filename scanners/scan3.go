package main

import (
	"fmt"
	"net"
	"sort"
)

var (
	scanPorts int = 100
	openPorts []int
)

func worker(ports, results chan int) {
	for p := range ports {
		fmt.Printf("--> scanning port %d\n", p)
		addr := fmt.Sprintf("scanme.nmap.org:%d", p)
		conn, err := net.Dial("tcp", addr)
		if err != nil {
			results <- 0
			continue // port is closed or filtered
		}
		conn.Close()
		results <- p
	}
}

func main() {
	ports := make(chan int, 100)
	results := make(chan int)
	for i := 0; i < cap(ports); i++ {
		go worker(ports, results)
	}

	go func() {
		for i := 1; i <= scanPorts; i++ {
			ports <- i
		}
	}()

	for i := 1; i <= scanPorts; i++ {
		port := <-results
		if port != 0 {
			openPorts = append(openPorts, port)
		}
	}
	close(ports)
	close(results)
	sort.Ints(openPorts)
	for _, p := range openPorts {
		fmt.Printf("open %d\n", p)
	}
}
