package main

import (
	"io/ioutil"
	"log"
	"os"

	"golang.org/x/crypto/ssh"
)

// A session can only perform one action. Once you call Run(), Output(), CombinedOutput(), Start(), or Shell(),
// you can't use the session for executing any other commands. If you need to run multiple commands, you can string them together separated with a semicolon.
// df -h; ps aux; pwd; whoami;

var username = "username"
var host = "example.com:22"
var privateKeyFile = "/home/user/.ssh/id_rsa"
var commandToExecute = "hostname"

func getKeySigner(privateKeyFile string) ssh.Signer {
	privateKeyData, err := ioutil.ReadFile(privateKeyFile)
	if err != nil {
		log.Fatal("error loading private key file. ", err)
	}

	privateKey, err := ssh.ParsePrivateKey(privateKeyData)
	if err != nil {
		log.Fatal("error parsing private key. ", err)
	}
	return privateKey
}

func main() {
	privateKey := getKeySigner(privateKeyFile)
	config := &ssh.ClientConfig{
		User: username,
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(privateKey),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	client, err := ssh.Dial("tcp", host, config)
	if err != nil {
		log.Fatal("error dialing server. ", err)
	}

	// Multiple sessions per client are allowed
	session, err := client.NewSession()
	if err != nil {
		log.Fatal("failed to create session: ", err)
	}
	defer session.Close()

	// Pipe the session output directly to standard output
	// Thanks to the convenience of writer interface
	session.Stdout = os.Stdout

	err = session.Run(commandToExecute)
	if err != nil {
		log.Fatal("error executing command. ", err)
	}
}
