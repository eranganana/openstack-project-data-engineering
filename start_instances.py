# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

if __name__ == "__main__":
    flavor = "ssc.medium" 
    private_net = "UPPMAX 2024/1-4 Internal IPv4 Network"
    floating_ip_pool_name = None
    floating_ip = None
    image_name = "Ubuntu 20.04 - 2023.12.07"

    identifier = random.randint(1000,9999)

    loader = loading.get_plugin_loader('password')

    auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                    username=env['OS_USERNAME'],
                                    password=env['OS_PASSWORD'],
                                    project_name=env['OS_PROJECT_NAME'],
                                    project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                    #project_id=env['OS_PROJECT_ID'],
                                    user_domain_name=env['OS_USER_DOMAIN_NAME'])

    sess = session.Session(auth=auth)
    nova = client.Client('2.1', session=sess)
    print ("user authorization completed.")

    image = nova.glance.find_image(image_name)

    flavor = nova.flavors.find(name=flavor)

    if private_net != None:
        net = nova.neutron.find_network(private_net)
        nics = [{'net-id': net.id}]
    else:
        sys.exit("private-net not defined.")

    #print("Path at terminal when executing this file")
    #print(os.getcwd() + "\n")
    prod_cfg_file_path =  os.getcwd()+'/prod-cloud-cfg.txt'
    if os.path.isfile(prod_cfg_file_path):
        userdata_prod = open(prod_cfg_file_path)
    else:
        sys.exit("prod-cloud-cfg.txt is not in current working directory")

    dev_cfg_file_path =  os.getcwd()+'/prod-cloud-cfg.txt'
    if os.path.isfile(dev_cfg_file_path):
        userdata_dev = open(dev_cfg_file_path)
    else:
        sys.exit("prod-cloud-cfg.txt is not in current working directory")
        
    cfg_file_path_1 =  os.getcwd()+'/node1-cloud-cfg.txt'
    if os.path.isfile(cfg_file_path_1):
        userdata_node_1 = open(cfg_file_path_1)
    else:
        sys.exit("node1-cloud-cfg.txt is not in current working directory")

    cfg_file_path_2 =  os.getcwd()+'/node2-cloud-cfg.txt'
    if os.path.isfile(cfg_file_path_2):
        userdata_node_2 = open(cfg_file_path_2)
    else:
        sys.exit("node2-cloud-cfg.txt is not in current working directory")

    cfg_file_path_3 =  os.getcwd()+'/node3-cloud-cfg.txt'
    if os.path.isfile(cfg_file_path_3):
        userdata_node_3 = open(cfg_file_path_3)
    else:
        sys.exit("node3-cloud-cfg.txt is not in current working directory")

    secgroups = ['default']

    print ("Creating instances ... ")
    instance_prod = nova.servers.create(name="group_14_production_server", image=image, flavor=flavor, key_name='Albin_DE',userdata=userdata_prod, nics=nics,security_groups=secgroups)
    instance_dev = nova.servers.create(name="group_14_development_server", image=image, flavor=flavor, key_name='Albin_DE',userdata=userdata_dev, nics=nics,security_groups=secgroups)
    instance_node_1 = nova.servers.create(name="group_14_node_"+str(identifier), image=image, flavor=flavor, key_name='Albin_DE',userdata=userdata_node_1, nics=nics,security_groups=secgroups)
    instance_node_2 = nova.servers.create(name="group_14_node_"+str(identifier+1), image=image, flavor=flavor, key_name='Albin_DE',userdata=userdata_node_2, nics=nics,security_groups=secgroups)
    instance_node_3 = nova.servers.create(name="group_14_node_"+str(identifier+2), image=image, flavor=flavor, key_name='Albin_DE',userdata=userdata_node_3, nics=nics,security_groups=secgroups)
    
    inst_status_prod = instance_prod.status
    inst_status_dev = instance_dev.status
    inst_status_node_1 = instance_node_1.status
    inst_status_node_2 = instance_node_2.status
    inst_status_node_3 = instance_node_3.status

    print ("waiting for 10 seconds.. ")
    time.sleep(10)

    while inst_status_prod == 'BUILD' or inst_status_dev == 'BUILD' or inst_status_node_1 == 'BUILD' or inst_status_node_2 == 'BUILD' or inst_status_node_3 == 'BUILD':
        print ("Instance: "+instance_prod.name+" is in "+inst_status_prod+" state, sleeping for 5 seconds more...")
        print ("Instance: "+instance_dev.name+" is in "+inst_status_dev+" state, sleeping for 5 seconds more...")
        print ("Instance: "+instance_node_1.name+" is in "+inst_status_node_1+" state, sleeping for 5 seconds more...")
        print ("Instance: "+instance_node_2.name+" is in "+inst_status_node_2+" state, sleeping for 5 seconds more...")
        print ("Instance: "+instance_node_3.name+" is in "+inst_status_node_3+" state, sleeping for 5 seconds more...")
        time.sleep(5)
        instance_prod = nova.servers.get(instance_prod.id)
        inst_status_prod = instance_prod.status
        instance_dev = nova.servers.get(instance_dev.id)
        inst_status_dev = instance_dev.status
        instance_node_1 = nova.servers.get(instance_node_1.id)
        inst_status_node_1 = instance_node_1.status
        instance_node_2 = nova.servers.get(instance_node_2.id)
        inst_status_node_2 = instance_node_2.status
        instance_node_3 = nova.servers.get(instance_node_3.id)
        inst_status_node_3 = instance_node_3.status


    ip_address_prod = None
    for network in instance_prod.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address_prod = network
            break
    if ip_address_prod is None:
        raise RuntimeError('No IP address assigned!')

    ip_address_dev = None
    for network in instance_dev.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address_dev = network
            break
    if ip_address_dev is None:
        raise RuntimeError('No IP address assigned!')
    
    ip_address_node_1 = None
    for network in instance_node_1.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address_node_1 = network
            break
    if ip_address_node_1 is None:
        raise RuntimeError('No IP address assigned!')

    ip_address_node_2 = None
    for network in instance_node_2.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address_node_2 = network
            break
    if ip_address_node_2 is None:
        raise RuntimeError('No IP address assigned!')

    ip_address_node_3 = None
    for network in instance_node_3.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address_node_3 = network
            break
    if ip_address_node_2 is None:
        raise RuntimeError('No IP address assigned!')

    print ("Instance: "+ instance_prod.name +" is in " + inst_status_prod + " state" + " ip address: "+ ip_address_prod)
    print ("Instance: "+ instance_dev.name +" is in " + inst_status_dev + " state" + " ip address: "+ ip_address_dev)
    print ("Instance: "+ instance_node_1.name +" is in " + inst_status_node_1 + " state" + " ip address: "+ ip_address_node_1)
    print ("Instance: "+ instance_node_2.name +" is in " + inst_status_node_2 + " state" + " ip address: "+ ip_address_node_2)
    print ("Instance: "+ instance_node_3.name +" is in " + inst_status_node_3 + " state" + " ip address: "+ ip_address_node_3)


    # Content for hosts.ini
    hosts_content = f"""
    [servers]
    prod ansible_host={ip_address_prod}
    dev ansible_host={ip_address_dev}
    node1 ansible_host={ip_address_node_1}
    node2 ansible_host={ip_address_node_2}
    node3 ansible_host={ip_address_node_3}

    [all:vars]
    ansible_python_interpreter=/usr/bin/python3

    [production]
    prod ansible_connection=ssh ansible_user=ubuntu

    [development]
    dev ansible_connection=ssh ansible_user=ubuntu
    
    [ray_workers]
    node1 ansible_connection=ssh ansible_user=ubuntu
    node2 ansible_connection=ssh ansible_user=ubuntu
    node3 ansible_connection=ssh ansible_user=ubuntu
    """

    # Overwrite hosts.ini file
    with open('ansible/hosts.ini', 'w') as file:
        file.write(hosts_content)
