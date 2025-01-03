// Search through a URL and find mailto links with email addresses
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
)

func main() {
	// Load command line arguments
	if len(os.Args) != 2 {
		fmt.Println("search for emails in a URL")
		fmt.Println("usage: " + os.Args[0] + " <url>")
		fmt.Println("example: " + os.Args[0] + " https://www.foobar.com")
		os.Exit(1)
	}
	url := os.Args[1]
	// Fetch the URL
	response, err := http.Get(url)
	if err != nil {
		log.Fatal("error fetching URL. ", err)
	}
	// Read the response
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal("error reading HTTP body. ", err)
	}
	// Look for mailto: links using a regular expression
	re := regexp.MustCompile("\"mailto:.*?[?\"]")
	matches := re.FindAllString(string(body), -1)
	if matches == nil {
		// Clean exit if no matches found
		fmt.Println("no emails found.")
		os.Exit(0)
	}
	// Print all emails found
	for _, match := range matches {
		// Remove "mailto prefix and the trailing quote or question mark
		// by performing a slice operation to extract the substring
		cleanedMatch := match[8 : len(match)-1]
		fmt.Println(cleanedMatch)
	}
}
