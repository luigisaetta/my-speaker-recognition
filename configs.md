## Configuration
Before starting the REST service, you need to do some small steps to configure it.

Global configuration is defined in config.py

### Local or Cloud?
As starting point, the easiest way to run the REST service is in **local** mode. Local mode was born to enable to run the REST service on our Mac (or laptop). It doesn't need the Objct Storage.

To configure for using local mode you need to set:
* CONFIG_TYPE = "local"

### Home directory
You need to define the base directory. It is where model.h5 is located. In addition, if you're using local model, it is the directory where the "audio db" json file is located.

Set:
* BASE_DIR = "absolute path where model.h5 and python files are located"
