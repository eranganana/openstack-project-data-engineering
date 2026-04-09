#!/bin/bash

# Path to the hosts.ini file
hosts_file="ansible/hosts.ini"

# Check if the hosts.ini file exists
if [ -f "$hosts_file" ]; then
    # Read the hosts.ini file line by line
    while IFS= read -r line; do
        # Check if the line contains 'prod' or 'dev' followed by ansible_host
        if grep -q "prod ansible_host=" <<< "$line"; then
            prod=$(grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" <<< "$line")
        elif grep -q "dev ansible_host=" <<< "$line"; then
            dev=$(grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" <<< "$line")
        fi
    done < "$hosts_file"

    # Export env variables
    echo "export PRODUCTION_SERVER=$prod" >> ~/.bashrc
    echo "export DEVELOPMENT_SERVER=$dev" >> ~/.bashrc
    echo "Environment variables exported to ~/.bashrc"

else
    echo "Error: hosts.ini file not found."
    exit 1
fi
