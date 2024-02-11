#!/bin/bash

function extractPorts(){
    ip_address=$(cat allPorts | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort -u)
    open_ports=$(cat allPorts | grep -op '\d{1,5}/open' | awk '{print $1}' FS="/" | xargs | tr ' ' ',')
    echo "IP Address: $ip_address"
    echo "Open ports: $open_ports"

    # sudo apt install xclip
    #echo $open_ports | tr -d '\n' | xclip -sel clip
}
