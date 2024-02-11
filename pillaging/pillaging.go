package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

var regexes = []*regexp.Regexp{
	regexp.MustCompile(`(?i)user`),
	regexp.MustCompile(`(?i)pass`),
	regexp.MustCompile(`(?i)kdb`),
	regexp.MustCompile(`(?i)login`),
	regexp.MustCompile(`(?i)secret`),
	regexp.MustCompile(`(?i)cred`),
	regexp.MustCompile(`(?i)access`),
	regexp.MustCompile(`(?i)key`), // keytab
	regexp.MustCompile(`(?i)token`),
	regexp.MustCompile(`(?i)ssh`),
	regexp.MustCompile(`(?i)rsa`),
}

func walkFn(path string, f os.FileInfo, err error) error {
	folders := strings.Split(path, "/")
	file := folders[len(folders)-1]
	for _, r := range regexes {
		if r.MatchString(file) {
			fmt.Printf("[+] HIT: %s\n", path)
		}
	}
	return nil
}

func main() {
	root := os.Args[1]
	if err := filepath.Walk(root, walkFn); err != nil {
		log.Panicln(err)
	}
}
