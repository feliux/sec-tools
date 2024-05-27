package main

import (
	"bytes"
	"context"
	"errors"
	"flag"
	"io"
	"log"
	"os"
	"strings"

	"github.com/projectdiscovery/subfinder/v2/pkg/runner"
)

var (
	domain, fileName                     string
	threads, timeout, maxEnumerationTime int
)

func init() {
	flag.IntVar(&threads, "threads", 10, "Thread controls the number of threads to use for active enumerations")
	flag.IntVar(&timeout, "timeout", 30, "Timeout is the seconds to wait for sources to respond")
	flag.IntVar(&maxEnumerationTime, "met", 10, "MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration")
	flag.StringVar(&domain, "d", "", "Domain for make enumeration")
	flag.StringVar(&fileName, "f", "", "Path to file containing domain lists")
	flag.Parse()
	log.SetFlags(0) // disable timestamps in logs / configure logger
}

func isDomain(domain string) bool {
	if len(strings.Split(domain, ".")) > 1 {
		return true
	}
	return false
}

func isFile(fileName string) bool {
	// _, err := os.Stat(fileName)
	// if err != nil {
	// 	if errors.Is(err, os.ErrNotExist) {
	// 		return false, err
	// 	} else {
	// 		return true, err
	// 	}
	// }
	// return true, nil
	if _, err := os.Stat(fileName); errors.Is(err, os.ErrNotExist) {
		return false
	}
	return true
}

func main() {
	if domain == "" && fileName == "" {
		log.Fatalln("you must provide -d(omain) or -f(ile) argument. Type -h for help")
	}
	if domain != "" && fileName != "" {
		log.Fatalln("you must provide just one argument between -d(omain) or -f(ile). Type -h for help")
	}
	subfinderOpts := &runner.Options{
		Threads:            threads,
		Timeout:            timeout,
		MaxEnumerationTime: maxEnumerationTime,
		// ResultCallback: func(s *resolve.HostEntry) {
		// callback function executed after each unique subdomain is found
		// },
		// ProviderConfig: "your_provider_config.yaml",
		// and other config related options
	}
	subfinder, err := runner.NewRunner(subfinderOpts)
	if err != nil {
		log.Fatalf("failed to create subfinder runner: %v", err)
	}
	output := &bytes.Buffer{}

	if isDomain(domain) {
		if err = subfinder.EnumerateSingleDomainWithCtx(context.Background(), domain, []io.Writer{output}); err != nil {
			log.Fatalf("failed to enumerate single domain %s: %v", domain, err)
		}
	} else if isFile(fileName) {
		file, err := os.Open(fileName)
		if err != nil {
			log.Fatalf("error occurred reading file: %v", err)
		}
		defer func() {
			err := file.Close()
			if err != nil {
				log.Fatalf("error occurred closing file; %v", err)
			}
		}()
		if err = subfinder.EnumerateMultipleDomainsWithCtx(context.Background(), file, []io.Writer{output}); err != nil {
			log.Fatalf("failed to enumerate subdomains from file: %v", err)
		}
	} else {
		log.Println("can not obtain domain from arguments. Please check the command executed")
	}
	log.Println(output.String())
}
