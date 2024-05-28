package main

import (
	"fmt"
	"log"
	"os"
	"os/user"
	"strconv"
)

func main() {
	// Check command line arguments
	if len(os.Args) != 4 {
		fmt.Println("change the owner of a file.")
		fmt.Println("usage: " + os.Args[0] + " <user> <group> <filepath>")
		fmt.Println("example: " + os.Args[0] + " dano dano test.txt")
		fmt.Println("example: sudo " + os.Args[0] + " root root test.txt")
		os.Exit(1)
	}
	username := os.Args[1]
	groupname := os.Args[2]
	filePath := os.Args[3]

	// Look up user based on name and get ID
	userInfo, err := user.Lookup(username)
	if err != nil {
		log.Fatal("error looking up user "+username+". ", err)
	}
	uid, err := strconv.Atoi(userInfo.Uid)
	if err != nil {
		log.Fatal("error converting "+userInfo.Uid+" to integer. ", err)
	}

	// Look up group name and get group ID
	group, err := user.LookupGroup(groupname)
	if err != nil {
		log.Fatal("error looking up group "+groupname+". ", err)
	}
	gid, err := strconv.Atoi(group.Gid)
	if err != nil {
		log.Fatal("error converting "+group.Gid+" to integer. ", err)
	}

	fmt.Printf("changing owner of %s to %s(%d):%s(%d).\n",
		filePath, username, uid, groupname, gid)
	os.Chown(filePath, uid, gid)
}
