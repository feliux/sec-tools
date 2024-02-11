package main

import (
	//"bufio"
	"io"
	"log"
	"net"
)

const port string = ":20080"

/*
	func echo(conn net.Conn) {
		defer conn.Close()
		reader := bufio.NewReader(conn)
		s, err := reader.ReadString('\n')
		if err != nil {
			log.Fatalln("Unable to read data")
		}
		log.Printf("Read %d bytes: %s", len(s), s)
		log.Println("Writing data")
		writer := bufio.NewWriter(conn)
		if _, err := writer.WriteString(s); err != nil {
			log.Fatalln("Unable to write data")
		}
		writer.Flush()
	}
*/
func echo(conn net.Conn) {
	defer conn.Close()
	// Copy data from io.Reader to io.Writer via io.Copy().
	if _, err := io.Copy(conn, conn); err != nil {
		log.Fatalln("Unable to read/write data")
	}
}

func main() {
	// Bind to TCP port 20080 on all interfaces.
	listener, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalln("Unable to bind to port")
	}
	log.Printf("Listening on 0.0.0.0:%s", port)
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
