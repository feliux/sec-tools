package main

import (
	"fmt"
	"net"
	"sync"
)

var (
	wg sync.WaitGroup
)

func isNetConnClosedErr(err error) bool {
	switch {
	case
		errors.Is(err, net.ErrClosed),
		errors.Is(err, io.EOF),
		errors.Is(err, syscall.EPIPE):
		return true
	default:
		return false
	}
}

func main() {
	for i := 1; i <= 100; i++ {
		wg.Add(100)
		go func(p int, wg *sync.WaitGroup) {
			defer wg.Done()
			fmt.Printf("--> scanning port %d\n", p)
			addr := fmt.Sprintf("scanme.nmap.org:%d", p)
			conn, err := net.Dial("tcp", addr)
			if err != nil {
				fmt.Printf("port %d is closed or filtered.\n", p)
			} else {
				conn.Close()
				fmt.Printf("%d open.\n", p)
			}
			isNetConnClosedErr(err)
			return
		}(i, &wg)
	}
	wg.Wait()
}
