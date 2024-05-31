package main

import (
	"context" // Done() struct{} || <- ctx.Done()
	"flag"
	"fmt"
	"net"
	"strconv"
	"strings"
	"sync"
	"time"
)

/*
Usage

$ go build -ldflags "-s -w" fastTCPScan.go // delete debugging information and symbol table
$ upx brute fastTCPScan

Could be configured to scan UDP
*/
var (
	host    = flag.String("h", "127.0.0.1", "Host or IP to scan (default 127.0.0.1)")
	ports   = flag.String("r", "1-65535", "Port range to scan: 80,443,1-65535,1000-2000,...")
	threads = flag.Int("t", 1000, "Threads number (default 1000).")
	timeout = flag.Duration("to", 1*time.Second, "Timeout seconds by port (default 1 sec).")
)

// Format range ports
func processRange(ctx context.Context, portString string) chan int {
	c := make(chan int)
	done := ctx.Done()
	go func() {
		var minPort, maxPort int
		var err error
		defer close(c)
		blocks := strings.Split(portString, ",")
		for _, block := range blocks {
			ipRange := strings.Split(block, "-")
			minPort, err = strconv.Atoi(ipRange[0])
			if err != nil {
				fmt.Printf("Could not interpret the range: %s", block)
				continue
			}
			if len(ipRange) == 1 {
				maxPort = minPort
			} else {
				maxPort, err = strconv.Atoi(ipRange[1])
				if err != nil {
					fmt.Printf("Could not interpret the range: %s", block)
					continue
				}
			}
			for port := minPort; port <= maxPort; port++ {
				select {
				case c <- port:
				case <-done:
					return
				}
			}
		}
	}()
	return c
}

// Scan ports concurrently
func scanPorts(ctx context.Context, in <-chan int) chan string {
	out := make(chan string)
	done := ctx.Done()
	var wg sync.WaitGroup
	wg.Add(*threads)
	for i := 0; i < *threads; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for {
				select {
				case port, ok := <-in:
					if !ok {
						return
					}
					scanResult := scanPort(port)
					select {
					case out <- scanResult:
					case <-done:
						return
					}
				case <-done:
					return
				}
			}
		}()
	}
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

// Scan a single port
func scanPort(port int) string {
	addr := fmt.Sprintf("%s:%d", *host, port)
	conn, err := net.DialTimeout("tcp", addr, *timeout)
	if err != nil {
		return fmt.Sprintf("%d: %s", port, err.Error())
	}
	conn.Close()
	return fmt.Sprintf("%d: Open", port)
}

func main() {
	flag.Parse()
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	fmt.Printf("\n[*] Scanning host %s (Ports: %s)\n", *host, *ports)
	pR := processRange(ctx, *ports)
	sP := scanPorts(ctx, pR)
	for port := range sP {
		/*
			if strings.HasSuffix(port, ": Open") {
				fmt.Println(port)
			}
		*/
		fmt.Println(port)
	}
}
