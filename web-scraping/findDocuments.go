// Load a URL and list all documents
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

var documentExtensions = []string{"doc", "docx", "pdf", "csv", "xls", "xlsx", "zip", "gz", "tar"}

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
	// Find and print all links that contain a document
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		href, exists := s.Attr("href")
		if exists && linkContainsDocument(href) {
			fmt.Println(href)
		}
	})
}

func linkContainsDocument(url string) bool {
	// Split URL into pieces
	urlPieces := strings.Split(url, ".")
	if len(urlPieces) < 2 {
		return false
	}
	// Check last item in the split string slice (the extension)
	for _, extension := range documentExtensions {
		if urlPieces[len(urlPieces)-1] == extension {
			return true
		}
	}
	return false
}
