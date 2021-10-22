## Speaker Recognition Service
This repository is used to prepare all docs and artefacts for the **MAD Hacks 2022**

### Features
* A Deep Learning model to extract features (embeddings) from an audio file, with the voice of a speaker
* a REST service that can be used to identify a speaker in a list of registered speakers
* a REST service with a set of functions (list, add, delete, restore) to manage the DB with registered speakers
* a really cool Web App with the UI to use and test all the functions
* some Data Science Notebooks with analysis on the embeddings

### Documentation
* [how to create the VM to run the REST service](./vm-creation.md)

### OCI Cloud services used
* OCI Compute VM
* OCI DataScience
* OCI Object Storage
* OCI Kubernetes Engine
* OCI Api Gateway


