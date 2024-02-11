package main

import (
	"fmt"
	"net"
	"sync"
)

var (
	wg sync.WaitGroup
)

func worker(ports chan int, wg *sync.WaitGroup) {
	for p := range ports {
		fmt.Printf("--> scanning port %d\n", p)
		addr := fmt.Sprintf("scanme.nmap.org:%d", p)
		conn, err := net.Dial("tcp", addr)
		if err != nil {
			continue // port is closed or filtered
		}
		conn.Close()
		fmt.Printf("%d open.\n", p)
		wg.Done()
	}
}

func main() {
	ports := make(chan int, 100)
	for i := 0; i < cap(ports); i++ {
		go worker(ports, &wg)
	}
	for i := 1; i <= 100; i++ {
		wg.Add(1)
		ports <- i
	}
	wg.Wait()
	close(ports)
}
