package main

import (
	"flag"
	"fmt"
	"net"
	"os"
)

var port string

func usage() {
	fmt.Fprintf(os.Stderr, "Usage: checkHostPort [port number]\n")
	flag.PrintDefaults()
}

func main() {
	flag.Usage = usage
	flag.StringVar(&port, "p", "8080", "Port to check.")
	flag.Parse()
	ln, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Can't listen on port %q: %s\n", port, err)
		os.Exit(1)
	}
	err = ln.Close()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't stop listening on port %q: %s\n", port, err)
		os.Exit(1)
	}
	fmt.Printf("TCP Port %q is available\n", port)
	os.Exit(0)
}
