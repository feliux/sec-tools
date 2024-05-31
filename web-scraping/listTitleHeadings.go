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
		fmt.Println("list all headings (h1-h6) in a web page")
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
	// Print title before headings
	title := doc.Find("title").Text()
	fmt.Printf("== title ==\n%s\n", title)
	// Find and list all headings h1-h6
	headingTags := [6]string{"h1", "h2", "h3", "h4", "h5", "h6"}
	for _, headingTag := range headingTags {
		fmt.Printf("== %s ==\n", headingTag)
		doc.Find(headingTag).Each(func(i int, heading *goquery.Selection) {
			fmt.Println(" * " + heading.Text())
		})
	}
}
