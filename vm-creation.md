## Creation of the environment to run the REST service

### Introduction
In this note we describe all the steps needed to create the VM and the Python Conda environment to run the REST service.

### VM requirements.
You need to create in Oracle Cloud (OCI) the following resources:
* a **VCN** with both a private and a public subnet. We strongly suggest you to use the wizard
* a **VM** Compute using as OS **Ubuntu 20.04**; You can choose the image in the Cloud repository
* a **bucket** in Object Storage called: audio_db

We suggest that the VM has at least: **2 OCPU and 16 GB Ram**; The shape we have used in our developments and tests is: VM.Standard.E2.2

The VM must be placed in the public subnet, to made it accessible from Internet using ssh and HTTP.

The image used is: Canonical-Ubuntu-20.04-2021.09.22-0

We suggest a boot volume of at least 50GB.

### Setup of the Conda environment
This are all the steps needed to create the right Python environment to run the REST service:

Install **Anaconda** distribution:
* connect through ssh, using ubuntu account
* cd /tmp
* wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
* bash /tmp/Anaconda3-2020.11-Linux-x86_64.sh

Accept all the default suggestions:
* accept license terms (yes)
* accept /home/ubuntu/anaconda3
* accept that the installer initialize Anaconda3 (yes)
* then exit and re-enter

At this point you should see the usual conda prompt:
* (base) ubuntu@yourvm-name:~$ 

Now, it is time to create the environment called **fastapi1**, with all the needed Python libraries.

For that we provide you the **environment.yml** file, in the speaker directory, containing the list of all Python packages that need to be installed.

Clone the github repository, then move in the speaker directory and execute the conda command

* conda env create --file environment.yml

To activate manually the environment fastapi1

* conda activate fastapi1

If you want that the environment fastapi1 becomes the default environment and have it available immediately after login (as ubuntu)
* modify .bashrc file
* add at the end the line: conda activate fastapi1


### Firewall
You need to open the needed ports in the on-board FW.

These are the commands:
* sudo iptables -I INPUT -p tcp -s 0.0.0.0/0 --dport 8888 -j ACCEPT
* sudo service netfilter-persistent save

In addition you need to create a security rule for the Public subnet where the VM is located.
You need to add an ingress rule, to allow the incoming traffic on PORT 8888.
If you specify 0.0.0.0 as source CIDR, you'll allow traffic from any IP. Otherwise, you can filter only IP from your client network.


