package main

import (
	"io"
	"log"
	"net"
)

const port string = ":20081"

// echo is a handler function that simply echoes received data.
func echo(conn net.Conn) {
	defer conn.Close()
	// Create a buffer to store received data.
	b := make([]byte, 512)
	for {
		// Receive data via conn.Read into a buffer.
		size, err := conn.Read(b[0:])
		if err == io.EOF {
			log.Println("Client disconnected")
			break
		}
		if err != nil {
			log.Println("Unexpected error")
			break
		}
		log.Printf("Received %d bytes: %s\n", size, string(b))
		// Send data via conn.Write.
		log.Println("Writing data")
		if _, err := conn.Write(b[0:size]); err != nil {
			log.Fatalln("Unable to write data")
		}
	}
}

/*
The main thread loops back and blocks on listener.Accept() while it
awaits another connection.

The handler goroutine, whose execution has been transferred to
the echo(net.Conn) function, proceeds to run, processing the data
*/

func main() {
	// Bind to TCP port 20080 on all interfaces.
	listener, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalln("Unable to bind to port")
	}
	log.Printf("Listening on 0.0.0.0%s", port)
	for {
		// Wait for connection. Create net.Conn on connection established.
		conn, err := listener.Accept() // function that blocks execution as it awaits client connections
		log.Println("Received connection")
		if err != nil {
			log.Fatalln("Unable to accept connection")
		}
		// Handle the connection. Using goroutine for concurrency.
		go echo(conn)
	}
}
