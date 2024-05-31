package main

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io"
	"os"
)

// Hashing is an important factor when it comes to protecting passwords.
// Other important factors are salting, using a cryptographically strong hash function,
// and the optional use of hash-based message authentication code (HMAC),
// which all add an additional secret key into the hashing algorithm.

func printUsage() {
	fmt.Println("usage: " + os.Args[0] + " <password>")
	fmt.Println("example: " + os.Args[0] + " Password1!")
}

func checkArgs() string {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}
	return os.Args[1]
}

// secretKey should be unique, protected, private,
// and not hard-coded like this. Store in environment var
// or in a secure configuration file.
// This is an arbitrary key that should only be used
// for example purposes.
var secretKey = "neictr98y85klfgneghre"

// generateSalt creates a salt string with 32 bytes of crypto/rand data
func generateSalt() string {
	randomBytes := make([]byte, 32)
	_, err := rand.Read(randomBytes)
	if err != nil {
		return ""
	}
	return base64.URLEncoding.EncodeToString(randomBytes)
}

// hashPassword hashes a password with the salt
func hashPassword(plainText string, salt string) string {
	hash := hmac.New(sha256.New, []byte(secretKey))
	io.WriteString(hash, plainText+salt)
	hashedValue := hash.Sum(nil)
	return hex.EncodeToString(hashedValue)
}

func main() {
	// Get the password from command line argument
	password := checkArgs()
	salt := generateSalt()
	hashedPassword := hashPassword(password, salt)
	fmt.Println("password: " + password)
	fmt.Println("salt: " + salt)
	fmt.Println("hashed password: " + hashedPassword)
}
