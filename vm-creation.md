## Creation of the environment to run the REST service

### Introduction
In this note we describe all the steps needed to create the VM and the Python Conda environment to run the REST service.

### VM requirements.
You need to create in Oracle Cloud (OCI) the following resources:
* a VCN with both a private and a public subnet. We strongly suggest you to use the wizard
* a VM Compute using as OS Ubuntu 20.04; You can choose the image in the Cloud repository
* a bucket in Object Storage called: audio_db

We suggest that the VM has at least: **2 OCPU and 16 GB Ram**; The shape we have used in our developments and tests is: VM.Standard.E2.2

The VM must be placed in the public subnet, to made it accessible from Internet using ssh and HTTP.

The image used is: Canonical-Ubuntu-20.04-2021.09.22-0

We suggest a boot volume of at least 50GB.

### Setup of the Conda environment
This all all the steps needed to create the right environment to run the REST service:

Install Anaconda distribution:
* connect through ssh using ubuntu account
* cd /tmp
* wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
* bash /tmp/Anaconda3-2020.11-Linux-x86_64.sh

Accept all the default suggestion.

