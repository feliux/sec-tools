#!/bin/bash

# machine_scan.sh 192.168.1

if [ $1 ]; then
    network=$1
    for i in $(seq 2 254); do
        timeout 1 bash -c "ping -c 1 $network.$i > /dev/null 2>&1" && echo "Available host $network.$i" &
    done; wait
else
    echo "Usage: ping_machine.sh <network: 192.168.1>\n"
    exit 1
fi
