package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"os"
)

func printUsage() {
	fmt.Println(os.Args[0] + `
Cryptographically sign a message using a private key.
Private key should be a PEM encoded RSA key.
Signature is generated using SHA256 hash.
Output signature is stored in filename provided.

Usage:
  ` + os.Args[0] + ` <privateKeyFilename> <messageFilename>   <signatureFilename>

Example:
  # Use priv.pem to encrypt msg.txt and output to sig.txt.256
  ` + os.Args[0] + ` priv.pem msg.txt sig.txt.256
`)
}

func checkArgs() (string, string, string) {
	// Need exactly 3 arguments provided
	if len(os.Args) != 4 {
		printUsage()
		os.Exit(1)
	}
	// Private key file name and message file name
	return os.Args[1], os.Args[2], os.Args[3]
}

// signMessage cryptographically signs a message creating a digital signature
// of the original message. Uses SHA-256 hashing.
func signMessage(privateKey *rsa.PrivateKey, message []byte) []byte {
	hashed := sha256.Sum256(message)
	signature, err := rsa.SignPKCS1v15(
		rand.Reader,
		privateKey,
		crypto.SHA256,
		hashed[:],
	)
	if err != nil {
		log.Fatal("error signing message. ", err)
	}
	return signature
}

// loadMessageFromFile loads the message that will be signed from file
func loadMessageFromFile(messageFilename string) []byte {
	fileData, err := ioutil.ReadFile(messageFilename)
	if err != nil {
		log.Fatal(err)
	}
	return fileData
}

// loadPrivateKeyFromPemFile loads the RSA private key from a PEM encoded file
func loadPrivateKeyFromPemFile(privateKeyFilename string) *rsa.PrivateKey {
	// Quick load file to memory
	fileData, err := ioutil.ReadFile(privateKeyFilename)
	if err != nil {
		log.Fatal(err)
	}
	// Get the block data from the PEM encoded file
	block, _ := pem.Decode(fileData)
	if block == nil || block.Type != "RSA PRIVATE KEY" {
		log.Fatal("unable to load a valid private key.")
	}
	// Parse the bytes and put it in to a proper privateKey struct
	privateKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		log.Fatal("error loading private key.", err)
	}
	return privateKey
}

// writeToFile saves data to file
func writeToFile(filename string, data []byte) error {
	// Open a new file for writing only
	file, err := os.OpenFile(
		filename,
		os.O_WRONLY|os.O_TRUNC|os.O_CREATE,
		0666,
	)
	if err != nil {
		return err
	}
	defer file.Close()
	_, err = file.Write(data)
	if err != nil {
		return err
	}
	return nil
}

// Sign a message using a private RSA key
func main() {
	// Get arguments from command line
	privateKeyFilename, messageFilename, sigFilename := checkArgs()
	// Load message and private key files from disk
	message := loadMessageFromFile(messageFilename)
	privateKey := loadPrivateKeyFromPemFile(privateKeyFilename)
	// Cryptographically sign the message
	signature := signMessage(privateKey, message)
	// Output to file
	writeToFile(sigFilename, signature)
}
