#!/bin/bash

# port_scan.sh 192.168.1.86

if [ $1 ]; then
    ip_address=$1
    for port in $(seq 1 65535); do
        timeout 1 bash -c "echo '' > /dev/tcp/$ip_address/$port"  2>/dev/null && echo "Open port: $port" &
    done; wait
else
    echo "Usage: scan_ports.sh <ip_address>\n"
    exit 1
fi
