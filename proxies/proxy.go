package main

import (
	"log"
	"net"
)

var localListenAddress = "localhost:9999"
var remoteHostAddress = "localhost:3000" // Not required to be remote

func main() {
	listener, err := net.Listen("tcp", localListenAddress)
	if err != nil {
		log.Fatal("error creating listener. ", err)
	}

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("error accepting connection. ", err)
		}
		go handleConnection(conn)
	}
}

// Forward the request to the remote host and pass response
// back to client
func handleConnection(localConn net.Conn) {
	// Create remote connection that will receive forwarded data
	remoteConn, err := net.Dial("tcp", remoteHostAddress)
	if err != nil {
		log.Fatal("error creating listener. ", err)
	}
	defer remoteConn.Close()

	// Read from the client and forward to remote host
	buf := make([]byte, 4096) // 4k buffer
	numBytesRead, err := localConn.Read(buf)
	if err != nil {
		log.Println("error reading from client.", err)
	}
	log.Printf(
		"forwarding from %s to %s:\n%s\n\n",
		localConn.LocalAddr(),
		remoteConn.RemoteAddr(),
		buf[0:numBytesRead],
	)
	_, err = remoteConn.Write(buf[0:numBytesRead])
	if err != nil {
		log.Println("error writing to remote host. ", err)
	}

	// Read response from remote host and pass it back to our client
	buf = make([]byte, 4096)
	numBytesRead, err = remoteConn.Read(buf)
	if err != nil {
		log.Println("error reading from remote host. ", err)
	}
	log.Printf(
		"passing response back from %s to %s:\n%s\n\n",
		remoteConn.RemoteAddr(),
		localConn.LocalAddr(),
		buf[0:numBytesRead],
	)
	_, err = localConn.Write(buf[0:numBytesRead])
	if err != nil {
		log.Println("error writing back to client.", err)
	}
}
