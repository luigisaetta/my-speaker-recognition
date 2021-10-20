## Creation of the environment to run the REST service

### Introduction
In this note we describe all the steps needed to create the VM and the Python Conda environment to run the REST service.

### VM requirements.
You need to create in Oracle Cloud (OCI) the following resources:
* a VCN with both a private and a public subnet. We strongly suggest you to use the wizard
* a VM Compute using as OS Ubuntu 20.04; You can choose the image in the Cloud repository
* a bucket in Object Storage called: audio_db

