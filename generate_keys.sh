#!/bin/bash

# Generate RSA SSH key pair without passphrase
ssh-keygen -t rsa -f ~/.ssh/key -N ""

# Copy the public key to dev-cloud-cfg.txt
echo "#cloud-config" > dev-cloud-cfg.txt
echo "users:" >> dev-cloud-cfg.txt
echo " - name: ubuntu" >> dev-cloud-cfg.txt
echo "   sudo: ALL=(ALL) NOPASSWD:ALL" >> dev-cloud-cfg.txt
echo "   home: /home/ubuntu" >> dev-cloud-cfg.txt
echo "   shell: /bin/bash" >> dev-cloud-cfg.txt
echo "   ssh_authorized_keys:" >> dev-cloud-cfg.txt
echo "     - $(cat ~/.ssh/key.pub)" >> dev-cloud-cfg.txt
echo "byobu_default: system" >> dev-cloud-cfg.txt

# Copy the public key to all other *-cloud-cfg.txt files
cp dev-cloud-cfg.txt prod-cloud-cfg.txt
cp dev-cloud-cfg.txt node1-cloud-cfg.txt
cp dev-cloud-cfg.txt node2-cloud-cfg.txt
cp dev-cloud-cfg.txt node3-cloud-cfg.txt

echo "Keys generated and copied successfully."
