package main

import (
	"bytes"
	"context"
	"io"
	"log"

	"github.com/projectdiscovery/subfinder/v2/pkg/runner"
)

const domain string = "hackerone.com"

func main() {
	subfinderOpts := &runner.Options{
		Threads:            10, // Thread controls the number of threads to use for active enumerations
		Timeout:            30, // Timeout is the seconds to wait for sources to respond
		MaxEnumerationTime: 10, // MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration
		// ResultCallback: func(s *resolve.HostEntry) {
		// callback function executed after each unique subdomain is found
		// },
		// ProviderConfig: "your_provider_config.yaml",
		// and other config related options
	}
	log.SetFlags(0) // disable timestamps in logs / configure logger
	subfinder, err := runner.NewRunner(subfinderOpts)
	if err != nil {
		log.Fatalf("Failed to create subfinder runner: %v", err)
	}
	output := &bytes.Buffer{}
	if err = subfinder.EnumerateSingleDomainWithCtx(context.Background(), domain, []io.Writer{output}); err != nil {
		log.Fatalf("Failed to enumerate single domain %s: %v", domain, err)
	}
	log.Println(output.String()) // print the output
}
