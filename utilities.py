#
# Utility functions, especially for tests
# updated:  18/10/2021
# based on some code from https://github.com/philipperemy/deep-speaker
#
import numpy as np
import json
from json import JSONEncoder
import os
import logging
import shutil
import ocifs

# global configs
import config

# our new utilities
from audio_utils_new import sample_from_mfcc, read_mfcc_io

from constants import SAMPLE_RATE, NUM_FRAMES

# the DL model
from conv_models import DeepSpeakerModel

# encoder used for saving the dictionary in a json format
class NumpyArrayEncoder(JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

#
# log settings
#
log = logging.getLogger("server")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', 
    level=os.environ.get("LOGLEVEL", "INFO"), datefmt='%Y-%m-%d %H:%M:%S')

# add the BASE_DIR (taken from config) to fname
def create_path(fname):
    BASE_DIR = config.global_settings['BASE_DIR']
    path = BASE_DIR + "/" + fname

    return path

#
# distance defined on cosine similarity: return dist = (1 - cos_simil)
#
def distance_cosine_similarity(x1, x2):
    # if similar speaker return a number close to 0
    s = np.sum(np.multiply(x1, x2), axis=1)

    # as vectors have length 1, we don't need to divide by norm (as it is 1)
    return abs(1. - s)

#
# get list of speakers name as list
#
def get_list_speakers_names(centroids, ordered):
    list_speakers = []

    for key in centroids.keys():
        list_speakers.append(key)
    
    if ordered:
        list_speakers = sorted(list_speakers)
    
    return list_speakers
#
# loads the centroids file from local fs
# this function is used if CONFIG = local
#
def load_centroids_from_local():
    CENTROIDS_FILE_NAME = config.global_settings['CENTROIDS_FILE_NAME']

    log.info("Loading centroids file from local")

    with open(create_path(CENTROIDS_FILE_NAME), 'r') as fp:
        new_centroids = json.load(fp)
    
    log.info("Checking centroids file")
    check_centroids_file(new_centroids)

    return new_centroids
#
# loads the centroids file from Object Storage
# this function is used if CONFIG = cloud
#
def load_centroids_from_oss():
    BUCKET_PREFIX = config.global_settings['BUCKET_PREFIX']
    CENTROIDS_FILE_NAME = config.global_settings['CENTROIDS_FILE_NAME']
    F_NAME = BUCKET_PREFIX + CENTROIDS_FILE_NAME

    log.info("Loading centroids file from Object Storage")

    fs = ocifs.OCIFileSystem(config="~/.oci/config")
                   
    with fs.open(F_NAME) as fp:
        new_centroids = json.load(fp)

    log.info("Checking centroids file")
    check_centroids_file(new_centroids)

    return new_centroids

#
# writes the changed centroid file to Object Storage, using ocifs
# 
#
def write_new_centroids_to_oss(new_centroids: dict):
    BUCKET_PREFIX = config.global_settings['BUCKET_PREFIX']
    NEW_CENTROIDS_FILE_NAME = config.global_settings['NEW_CENTROIDS_FILE_NAME']

    log.info("Writing new centroids to Object Storage")

    check_centroids_file(new_centroids)

    fs = ocifs.OCIFileSystem(config="~/.oci/config")

    with fs.open(BUCKET_PREFIX + NEW_CENTROIDS_FILE_NAME, mode="w") as fp:
                json.dump(new_centroids, fp, cls=NumpyArrayEncoder)

#
# writes the changed centroid file to local fs
# 
#
def write_new_centroids_to_local(new_centroids: dict):
    NEW_CENTROIDS_FILE_NAME = config.global_settings['NEW_CENTROIDS_FILE_NAME']

    log.info("Writing centroids to local")

    check_centroids_file(new_centroids)

    with open(create_path(NEW_CENTROIDS_FILE_NAME), 'w') as fp:
                json.dump(new_centroids, fp, cls=NumpyArrayEncoder)
#
# loads the new_centroids file, to check it
#
def load_centroids_newfile():
    # always from local fs
    CENTROIDS_FILE_NAME = config.global_settings['NEW_CENTROIDS_FILE_NAME']

    # with CONFIG_TYPE we manage the different storage in Cloud (Object storage)
    # and locally (on fs)
    
    with open(create_path(CENTROIDS_FILE_NAME), 'r') as fp:
        new_centroids = json.load(fp)         

    log.info("Number of distinct speakers: " + str(len(new_centroids)))

    # check the content
    if check_centroids_file(new_centroids) == False:
        log.error("Error: Anomaly in centroid file, one of the embedding vector has not the expected size!")
    else:
        log.info("Embedding vectors size OK!")

    return new_centroids

#
# do some checks on the content of the centroid file
# to be called after load_centroids
#
def check_centroids_file(centroids):
    isOK = True
    EPS = 0.0001

    log.info("Checking embeddings size and norm")

    # check that all vectors have size EMBEDDING_DIMS
    for key in centroids.keys():
        if len(centroids[key][0]) != config.global_settings['EMBEDDING_DIMS']:
            log.error("Embedding size is not OK")
            isOK = False
    
    if isOK:
        log.info("Embeddings size (512) OK")

    # check that all vector have norm = 1
    for key in centroids.keys():
        vec = np.array(centroids[key][0])
        norm = np.linalg.norm(vec)

        if abs(norm - 1.0) > EPS:
            log.error("Error: norm is not 1")
            isOK = False

    if isOK:
        log.info("Embeddings vector norm OK")

    return isOK

#
# save new wav file
#
def save_wav(name, file: bytes):
    print("saving file for:", name)

    FNAME = name + ".wav"
    FPATH = create_path(FNAME)

    f = open(FPATH, 'wb')
    f.write(file)
    f.close()

    return

def read_wav(file_name):
    FPATH = create_path(file_name)

    with open(FPATH, "rb") as f:
        # read the entire file, is small (1000 points)
        bytes_read = f.read()
    
    return bytes_read

#
# Compute the embeddings vector for the wav
# as input bytes read from wav
#
def compute_embeddings(file: bytes, model):
     # compute mel cepstral coeff (mfcc)
    mfcc = sample_from_mfcc(read_mfcc_io(file, SAMPLE_RATE), NUM_FRAMES)
        
    if config.global_settings['IS_DEBUG']:
            print('MFCC shape is:', mfcc.shape)
        
    # compute the embedding vector
    embedding = model.m.predict(np.expand_dims(mfcc, axis=0))
        
    if config.global_settings['IS_DEBUG']:
        print('Embedding shape is:', embedding.shape)
    
    # check the shape
    if embedding.shape[1] != config.global_settings['EMBEDDING_DIMS']:
        log.error("Invalid embedding shape...")
    else:
        log.info("Embedding shape OK")

    return embedding

#
# for print
#
def print_dict(diz):
    print()
    print("Result is:")
    print(diz)

    return

def swap_centroids_files_local():
    # rename centroids file as centroids.bck
    # rename new_centroids file as centroids

    BCK_PATH = create_path(config.global_settings['BCK_CENTROIDS_FILE_NAME'])
    NEW_PATH = create_path(config.global_settings['NEW_CENTROIDS_FILE_NAME'])
    CUR_PATH = create_path(config.global_settings['CENTROIDS_FILE_NAME'])

    # backup CUR as BCK
    log.info("backup CUR as BCK")
    shutil.copyfile(CUR_PATH, BCK_PATH)

    # copy NEW as CUR
    log.info("copy NEW as CUR")
    shutil.copyfile(NEW_PATH, CUR_PATH)

def swap_centroids_files_oss():
    BUCKET_PREFIX = config.global_settings['BUCKET_PREFIX']
    BCK = config.global_settings['BCK_CENTROIDS_FILE_NAME']
    CUR = config.global_settings['CENTROIDS_FILE_NAME']
    NEW = config.global_settings['NEW_CENTROIDS_FILE_NAME']

    fs = ocifs.OCIFileSystem(config="~/.oci/config")

    # backup CUR as OLD
    log.info("backup CUR as BCK")

    # read CUR
    with fs.open(BUCKET_PREFIX + CUR, 'r') as fp:
        cur_centroids = json.load(fp)
    
    # write on BCK
    with fs.open(BUCKET_PREFIX + BCK, mode="w") as fp:
        json.dump(cur_centroids, fp, cls=NumpyArrayEncoder)

    # copy NEW as CUR
    log.info("copy NEW as CUR")

    # read NEW
    with fs.open(BUCKET_PREFIX + NEW, 'r') as fp:
        new_centroids = json.load(fp)
    
    # write on CUR
    with fs.open(BUCKET_PREFIX + CUR, mode="w") as fp:
        json.dump(new_centroids, fp, cls=NumpyArrayEncoder)
#
# handle the restore in case CONFIG local
#
def restore_centroids_from_bck_local():
    BCK_PATH = create_path(config.global_settings['BCK_CENTROIDS_FILE_NAME'])
    CUR_PATH = create_path(config.global_settings['CENTROIDS_FILE_NAME'])

    log.info("restore BCK as CUR")
    shutil.copyfile(BCK_PATH, CUR_PATH)

#
# handle the restore in case CONFIG cloud
#
def restore_centroids_from_bck_oss():
    BUCKET_PREFIX = config.global_settings['BUCKET_PREFIX']
    BCK = config.global_settings['BCK_CENTROIDS_FILE_NAME']
    CUR = config.global_settings['CENTROIDS_FILE_NAME']

    log.info("restore BCK as CUR")

    fs = ocifs.OCIFileSystem(config="~/.oci/config")

    with fs.open(BUCKET_PREFIX + BCK, 'r') as fp:
        new_centroids = json.load(fp)
    
    # write
    with fs.open(BUCKET_PREFIX + CUR, mode="w") as fp:
        json.dump(new_centroids, fp, cls=NumpyArrayEncoder)

    