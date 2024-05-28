package main

import (
	"io/ioutil"
	"log"

	"golang.org/x/crypto/ssh"
)

// Note that you can pass more than a single private key to the ssh.PublicKeys() function.
// It accepts an unlimited number of keys. If you provide multiple keys, and only one works for the server,
// it will automatically use the one key that works.
// This is useful if you want to use the same configuration to connect to a number of servers.
// You may want to connect to 1000 different hosts using 1000 unique private keys.
// Instead of having to create multiple SSH client configs, you can reuse a single config that contains all of the private keys.

var username = "username"
var host = "example.com:22"
var privateKeyFile = "/home/user/.ssh/id_rsa"

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
			ssh.PublicKeys(privateKey), // Pass 1 or more key
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	client, err := ssh.Dial("tcp", host, config)
	if err != nil {
		log.Fatal("error dialing server. ", err)
	}

	log.Println(string(client.ClientVersion()))
}
