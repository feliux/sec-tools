package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

func main() {
	// Load command line arguments
	if len(os.Args) != 2 {
		fmt.Println("list all words by frequency from a web page")
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

	doc, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal("error loading HTTP response body. ", err)
	}

	// Find and list all headings h1-h6
	wordCountMap := make(map[string]int)
	doc.Find("p").Each(func(i int, body *goquery.Selection) {
		fmt.Println(body.Text())
		words := strings.Split(body.Text(), " ")
		for _, word := range words {
			trimmedWord := strings.Trim(word, " \t\n\r,.?!")
			if trimmedWord == "" {
				continue
			}
			wordCountMap[strings.ToLower(trimmedWord)]++

		}
	})

	// Print all words along with the number of times the word was seen
	for word, count := range wordCountMap {
		fmt.Printf("%d | %s\n", count, word)
	}
}
