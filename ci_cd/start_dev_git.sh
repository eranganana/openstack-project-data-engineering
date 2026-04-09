#!/bin/bash

# Set the post-receive hook
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app
git init
cp /home/ubuntu/DE2-Project/development_server/* .
git remote add production ubuntu@$PRODUCTION_SERVER:/home/ubuntu/app