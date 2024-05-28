package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Println("change the permissions of a file.")
		fmt.Println("usage: " + os.Args[0] + " <mode> <filepath>")
		fmt.Println("example: " + os.Args[0] + " 777 test.txt")
		fmt.Println("example: " + os.Args[0] + " 0644 test.txt")
		os.Exit(1)
	}
	mode := os.Args[1]
	filePath := os.Args[2]

	// Convert the mode value from string to uin32 to os.FileMode
	fileModeValue, err := strconv.ParseUint(mode, 8, 32)
	if err != nil {
		log.Fatal("error converting permission string to octal value. ",
			err)
	}
	fileMode := os.FileMode(fileModeValue)
	err = os.Chmod(filePath, fileMode)
	if err != nil {
		log.Fatal("error changing permissions. ", err)
	}
	fmt.Println("Permissions changed for " + filePath)
}
