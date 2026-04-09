# Setup production and development servers
scp your `operrc` file from snic into the project folder, give it the name on the format `openrc_SUFFIX.sh`, you will be prompted for which rc-file to use whenever you interact with SNIC via the dedicated scripts

# Start servers
### This will launch the prod server, dev server and a dedicated Ray Cluster
```
cd DE2-Project
./start_servers.sh
```

# Delete servers
Simply run
```
source delete_servers.sh
``` 

# Access Flask App on local computer
Do
```
source ~/.bashrc
echo $PRODUCTION_SERVER
```

Enter the output into your LOCAL .ssh/config (make sure that the floating ip is correct)
```
Host node
    Hostname <floating IP to node>
    KexAlgorithms +diffie-hellman-group1-sha1
    User ubuntu
    IdentityFile <LOCAL KEY TO NODE>
    LocalForward 5100 127.0.0.1:5100

Host production
    Hostname <OUTPUT FROM $PRODUCTION_SERVER>
    User ubuntu
    IdentityFile ~/.ssh/key
    ProxyJump ubuntu@<floating IP to node>

```

ssh into node

```
ssh node
``` 

then ssh into production

```
source ~/.bashrc
ssh -i ~/.ssh/key ubuntu@$PRODUCTION_SERVER -L 5100:localhost:5100
```

In browser, enter `localhost:5100`

# Update model on development server
First, ssh into development server

```
source ~/.bashrc
ssh -i ~/.ssh/key ubuntu@$DEVELOPMENT_SERVER
```

Git hooks is connected via the /app directory
```
cd app
```

Here, the code can be altered (or change any code). Retrain a model. Store it with the name `model.pkl`.  
```
git config --global user.email <GH_EMAIL>
git config --global user.name <GH_USERNAME>

git add model.pkl
git commit -m "<your message>"
git push production master
```

When setting up a new cluster, the servers pulls the head of `DE2-Project`, so any changes there will be reflected on the deployment. However, for CI/CD, currently one needs to do updates via `/app` directory on development server