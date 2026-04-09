#!/bin/bash

# Get suffix for openstack rc file, source rc file
echo "Setup env for openstack"
read -p "Enter suffix for rc-file: " USERNAME
source openrc_$USERNAME.sh

# Get list of servers with name prefix "group_14_"
servers=$(openstack server list --name "group_14_" -f value -c ID)

# Loop through each server ID and delete it
for server_id in $servers; do
    echo "Deleting server $server_id..."
    openstack server delete $server_id
done

echo "All servers with name prefix 'group_14_' have been deleted."
