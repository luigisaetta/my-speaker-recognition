## The REST Service
At the heart of the **Speaker Recognition Service** there is a REST service that provides, both to the UI and to every other client, all the functionalities.

### Implementation: some notes
The REST service is running on a compute VM. 

It is implemented using FastAPI. With FastAPI it is really easy to create a REST interface, using Python code.

The main python module is server.py, that is the entry point for every HTTP request.

### REST accessible functionalities
The REST server provides access to these functionalities:
* add_speaker, enable to add a speaker to the "audio db", with the pairs (speaker_name, embedding)
* list_speakers, provides the list of registered speakers
* delete_speaker
* Identify, is the function that enable the recognition of a speaker, from a given audio clip

### Test UI
One of the nice feature of FastAPI is that it creates a nice UI, that can be used to test each individual function and for administration puprposes.
![ui](https://github.com/luigisaetta/my-speaker-recognition/blob/main/rest-ui.png)

FastAPI also create the Swagger doc for the REST service, simplifying integration with other clients.

### API Gateway
All the functionalities accessible through REST are exposed using an **OCI API Gateway**
