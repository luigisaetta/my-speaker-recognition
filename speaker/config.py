#
# This files contains global configurations
#

description = """
    **Speaker Identification API** helps you to identify a speaker from a short audio clip. 🚀

    You will be able to:

    * Identify the speaker
    * Verify if the speaker is in the DB
    * Add a speaker to the DB 
    * List the speakers in the DB
    * Reload the DB
    * Restore the centroids file
    * delete a speaker 
    """

global_settings = dict(
    VERSION = "0.7.1",

    # can be: local or cloud
    CONFIG_TYPE = "local",

    # bucket containing all the files from the model
    BUCKET_PREFIX = "oci://audio_db@frfbyzohecdc/",
    # dir containin all py and model files
    BASE_DIR = "/Users/lsaetta/Progetti/speaker",
    
    # enable/disable additional print for diagnostic
    IS_DEBUG = False,
    # max results in list produced by predict
    # limits the list of results with distance returned
    MAX_RESULTS = 5,
    # the port FastAPI is listening on
    PORT = 8888,
    # IP
    IP = "0.0.0.0",

    # the name of the file with all pairs name:embedding-vec
    CENTROIDS_FILE_NAME = "centroids_data_structure.json",
    # the new file, with speaker added
    NEW_CENTROIDS_FILE_NAME = "new_centroids_data_structure.json",
    BCK_CENTROIDS_FILE_NAME = "centroids_data_structure.json.bck",
    
    # Keras model file name
    MODEL_FILE = 'model.h5',
    # length of the embedding vector
    EMBEDDING_DIMS = 512,
    
    # used by verify: compare name with the name of the first NUM_CANDIDATES 
    NUM_CANDIDATES = 2,

    # description used by FastAPI
    TITLE = "Speaker Recognition Service",

    DESCRIPTION = description
)