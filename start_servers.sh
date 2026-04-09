#!/bin/bash
# Install dependecies
sudo apt update
sudo apt install -y python3-openstackclient python3-novaclient python3-keystoneclient
sudo apt-add-repository ppa:ansible/ansible
sudo apt update
sudo apt install -y ansible
sudo apt upgrade -y

# Delete existing servers
read -p "Enter suffix for rc-file: " USERNAME
source openrc_$USERNAME.sh

# Get list of servers with name prefix "group_14_"
servers=$(openstack server list --name "group_14_" -f value -c ID)

# Check if the servers variable is not empty
if [ -n "$servers" ]; then
  echo "Servers already up and running, delete with:"
  echo "        ./delete_servers.sh"
  exit 0
fi

# Generate keys for cluster
echo "Generating keys"
source generate_keys.sh

# Start new instances via openstack
echo "Starting instances"
python3 start_instances.py

# Store additional environment variables
echo "Store environment variables"
source store_env.sh

# Orchestrate instances with ansible
echo "Waiting for instances to be available with ssh, 30 seconds..."
sleep 30
export ANSIBLE_HOST_KEY_CHECKING=False
echo "Orchestrate instances with ansible playbook"
ansible-playbook -i ansible/hosts.ini ansible/configuration.yml --private-key=~/.ssh/key

echo "================ DONE ================"
echo "Production ip stored in PRODUCTION_SERVER environment variable"
echo "Development ip stored in DEVELOPMENT_SERVER environment variable"
echo "First do source ~/.bashrc"
echo "Access via ssh -i ~/.ssh/key ubuntu@$<ENV_VARIABLE>"
echo "See readme for how to access Flask app via ssh port forwarding"