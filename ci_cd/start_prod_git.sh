#!/bin/bash

# Set the post-receive hook
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app
git init --bare
touch hooks/post-receive
echo '#!/bin/bash
while read oldrev newrev ref
do
    if [[ $ref =~ .*/master$ ]];
    then
        echo "Master ref received. Deploying master branch to production..."
        
        # Define the directory where models are stored
        MODEL_DIR=/home/ubuntu/DE2-Project/production_server
        
        # Remove existing model files
        echo "Removing existing model files..."
        sudo rm -f $MODEL_DIR/model.*

        # Deploy the new master branch
        sudo git --work-tree=/home/ubuntu/DE2-Project/production_server --git-dir=/home/ubuntu/app checkout -f
    else
        echo "Ref $ref successfully received. Doing nothing: only the master branch may be deployed on this server."
    fi
done
' > hooks/post-receive

chmod +x hooks/post-receive