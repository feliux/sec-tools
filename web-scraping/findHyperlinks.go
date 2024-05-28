// Load a URL and list all links found
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/PuerkitoBio/goquery"
)

func main() {
	// Load command line arguments
	if len(os.Args) != 2 {
		fmt.Println("find all links in a web page")
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
	// Extract all links
	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal("error loading HTTP response body. ", err)
	}
	// Find and print all links
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		href, exists := s.Attr("href")
		if exists {
			fmt.Println(href)
		}
	})
}
