## Speaker Recognition Service
The Speaker Recognition Service provides you a set of functionalities to enable the recognition of a speaker from a short audio clip of his voice.

### Features
* A Deep Learning model to extract features (embeddings) from an audio file, with the voice of a speaker
* a REST service that can be used to identify a speaker in a list of registered speakers
* a REST service with a set of functions (list, add, delete, restore) to manage the DB with registered speakers
* a really cool Web App, built using Angular, with the UI to use and test all the functions
* some **Data Science** Notebooks with analysis on the embeddings

### Documentation
* [how to create the VM to run the REST service](./vm-creation.md)
* [the UI Frontend](./frontend.md)
* [the Speaker Recognition model](./speaker-rec-model.md)

### OCI Cloud Services used
The Speaker Recognition Model is entirely running on Oracle Cloud Infrastructure (OCI) and has been developed using the OCI services listed below, plus a set of Open Source technologies.

* OCI Compute VM
* OCI DataScience
* OCI Object Storage
* OCI Kubernetes Engine
* OCI Api Gateway

### Open Source
* Angular, Bootstrap, jQuery
* FastAPI
* Librosa, Pydub
* TensorFlow2 and Keras
* Numpy 

### Credits
The Deep Learning model is partially based on the work done by Philippe Remy.

The original code is available in the GitHub repository: https://github.com/philipperemy/deep-speaker
