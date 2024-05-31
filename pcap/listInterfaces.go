package main

import (
	"fmt"
	"log"

	"github.com/google/gopacket/pcap"
)

func main() {
	// Find all devices
	devices, err := pcap.FindAllDevs()
	if err != nil {
		log.Fatal(err)
	}
	// Print device information
	fmt.Println("devices found:")
	for _, device := range devices {
		fmt.Println("\nname: ", device.Name)
		fmt.Println("description: ", device.Description)
		fmt.Println("devices addresses: ", device.Description)
		for _, address := range device.Addresses {
			fmt.Println("- ip address: ", address.IP)
			fmt.Println("- subnet mask: ", address.Netmask)
		}
	}
}
