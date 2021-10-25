#!/usr/bin/env python

#
# REST server implementation
# author:   L. Saetta
# updated:  18/10/2021
# based on some code from https://github.com/philipperemy/deep-speaker
#
import io
import time
import os
import logging
import json
import uvicorn
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

# needed for the cloud, access to Object Storage
import oci
import ocifs

# global configurations in config.py
import config

# the DL model
from conv_models import DeepSpeakerModel

# code for adding new speakers to DB
from speaker_management import add_speaker

# utilities functions
from utilities import compute_embeddings, distance_cosine_similarity, print_dict
from utilities import load_centroids_newfile, save_wav, swap_centroids_files_local, swap_centroids_files_oss
from utilities import NumpyArrayEncoder, load_centroids_from_oss, load_centroids_from_local
from utilities import create_path, write_new_centroids_to_oss, write_new_centroids_to_local
from utilities import restore_centroids_from_bck_local, restore_centroids_from_bck_oss, get_list_speakers_names

#
# constants for audio processing
#
from constants import SAMPLE_RATE, NUM_FRAMES

#
# log settings
#
log = logging.getLogger("server")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', 
    level=os.environ.get("LOGLEVEL", "INFO"), datefmt='%Y-%m-%d %H:%M:%S')

log.info("Starting the server...")

#
# Functions
#

#
# load the pre-trained DL model
#
def load_model():
    log.info("Loading the DL model...")

    CONFIG_TYPE = config.global_settings['CONFIG_TYPE']
    MODEL_FILE = config.global_settings['MODEL_FILE']

    vmodel = DeepSpeakerModel()

    # renamed model file to model.h5 (was: ResCNN_triplet_training_checkpoint_265.h5)
    
    # continue to load local file
    # but the model is not changing.. do we need a special location?
    # we can continue to ship with the code !
    vmodel.m.load_weights(create_path(MODEL_FILE), by_name=True)

    return vmodel
#
# This loads the centroids file DB and handle the two cases: local, cloud CONFIG
#
def load_centroids():
    log.info("Loading the centroids DB...")

    CONFIG_TYPE = config.global_settings['CONFIG_TYPE']

    # with CONFIG_TYPE we manage the different storage in Cloud (Object storage)
    # and locally (on fs)
    if CONFIG_TYPE == "local":
        new_centroids = load_centroids_from_local()
    else:
        if CONFIG_TYPE == "cloud":
            new_centroids = load_centroids_from_oss()        

    log.info("Number of distinct speakers: " + str(len(new_centroids)))

    return new_centroids 

#
# swap centroid files
#
def swap_centroids_files():
    log.info("Swapping the centroids DB...")

    CONFIG_TYPE = config.global_settings['CONFIG_TYPE']

    if CONFIG_TYPE == "local":
        swap_centroids_files_local()
    else:
        if CONFIG_TYPE == "cloud":
            swap_centroids_files_oss()

#
# This handle the centroids file restore and handle the two cases: local, cloud CONFIG
#
def restore_centroids_from_bck():
    log.info("Restoring the centroids DB...")

    CONFIG_TYPE = config.global_settings['CONFIG_TYPE']

    # with CONFIG_TYPE we manage the different storage in Cloud (Object storage)
    # and locally (on fs)
    if CONFIG_TYPE == "local":
        restore_centroids_from_bck_local()
    else:
        if CONFIG_TYPE == "cloud":
            restore_centroids_from_bck_oss()        

    return 

# return the dictionary with all scores
# score is the distance between the current sound vector and the centroid
# current sound vector is in embedding
# list is limited to MAX_RESULTS
def compare_other_centroids(embedding, centroids):
    tmp_dict = {}
        
    for key in centroids.keys():
        dist = round(distance_cosine_similarity(embedding, centroids[key])[0], 3)
        tmp_dict[key] = dist
        
    # sort
    tmp_list = sorted(tmp_dict.items(), key=lambda x:x[1])
    # in tmp_list I have tuples like ('Lorenzo_DeMarchis', 0.278)

    # here I limit to MAX_RESULTS
    new_tmp_list = []

    for i, el in enumerate(tmp_list):
        if i < config.global_settings['MAX_RESULTS']:
            new_dict = {}
            # unpack the tuple
            new_dict['name'] = el[0]
            new_dict['result'] = el[1]
            new_tmp_list.append(new_dict)

    out_dict = {} 
    out_dict["result"] = new_tmp_list
    
    return out_dict

def compute_distances(embedding, centroids):
    dict_dist = {}
    
    for key in centroids.keys():
        dist = round(distance_cosine_similarity(embedding, centroids[key])[0], 3)

        dict_dist[key] = dist

    # sort
    tmp_list = sorted(dict_dist.items(), key=lambda x:x[1])
    
    # here I limit to MAX_RESULTS
    new_tmp_list = []

    for i, el in enumerate(tmp_list):
        if i < config.global_settings['MAX_RESULTS']:
            new_tmp_list.append(el)

    out_dict = dict(new_tmp_list)
    
    return out_dict



# load the DL model
model = load_model()

# load the centroids file
# file must be modified every time a new speaker is added
#
centroids = load_centroids()

# create the app
app = FastAPI(title=config.global_settings['TITLE'], version=config.global_settings['VERSION'], 
        description=config.global_settings['DESCRIPTION'])

#
# functions handling HTTP requests
#

#
# This is the function that handles the POST request for identification
# it expects a wav file in binary format as input
# and gives as output a JSON with pairs name:distance 
# where distance is the distance from the given input and the centroid for name
#
@app.post("/identify", tags=["Identification"]) 
def identify(file: bytes = File(...)):
    
    # for timing the request
    tStart = time.time()
    
    log.info('Identify: Received a request')

    try:
        embedding = compute_embeddings(file, model)
        
        # compare with all centroids
        out_dict = compare_other_centroids(embedding, centroids)
        
        print_dict(out_dict)
        
        tEla = time.time() - tStart
        print()
        print('Elapsed time (sec.)', round(tEla, 3))
        
    except Exception as e:
        print('The exception is:', e)
        print("Input is not a valid audio file!")
        raise HTTPException(status_code=415, detail="Unsupported file provided.") 
    
    return out_dict

@app.post("/verify", tags=["Identification"]) 
def verify(file: bytes = File(...)):

    # for timing the request
    tStart = time.time()
    
    log.info('Verify: Received a request')

    final_dict_out = {}

    try:
        embedding = compute_embeddings(file, model)
        
        # compare with all centroids
        out_dict = compare_other_centroids(embedding, centroids)

        # compute the summary result
        final_dict_out["summary"] = "false"
        final_dict_out["result"] = out_dict

        list_pair = out_dict["result"]

        for pair in list_pair:
            if pair["result"] < config.global_settings['THRESHOLD']:
                final_dict_out["summary"] = "true"
                break
        
        print_dict(final_dict_out)
        
        tEla = time.time() - tStart
        print()
        log.info('Elapsed time (sec.)', round(tEla, 3))
        
    except Exception as e:
        print('The exception is:', e)
        print("Input is not a valid audio file!")
        raise HTTPException(status_code=415, detail="Unsupported file provided.") 
    
    return final_dict_out

# By using @app.get("/") you are allowing the GET method to work for the / endpoint.
@app.get("/", tags=["Operation"])
def home():
    return "Congratulations! Your API is working. Now head over to http://localhost:8888/docs."

#
# return the list of registered speakers' names
# the list can be sorted
#
@app.get("/list_speakers", tags=["Operation"])
def list_speakers(ordered: str = "false"):
    global centroids

    log.info('List speakers: Received a request')
    
    list_speakers = get_list_speakers_names(centroids, ordered)

    out_dict = {}
    out_dict['speakers'] = list_speakers

    print_dict(out_dict)

    return out_dict
#
# This function handles the request for adding a new speaker to the DB
#
@app.post("/add_speaker", tags=["Operation"]) 
def add_new_speaker(name: str, file: bytes = File(...)):
    global centroids

    log.info("Adding speaker: "  + name)
    
    # for timing the request
    tStart = time.time()

    try:
        # save in a wav file in the local dir
        save_wav(name, file)

        filename = create_path(name + ".wav")

        # create the new_centroids structure
        new_centroids = add_speaker(name, filename, centroids, model)

        # if CONFIG = cloud must copy new centroids to OSS
        if config.global_settings['CONFIG_TYPE'] == "cloud":
            log.info("Writing new centroid to oss")
            write_new_centroids_to_oss(new_centroids)
        else:
            # local
            log.info("Writing new centroid to local")
            write_new_centroids_to_local(new_centroids)

        # swap the files (handles the double config cloud or local)
        log.info("Swap centroids files")
        swap_centroids_files()

        # reload
        log.info("Reload centroids")
        centroids = load_centroids()

        out_dict = {}
        out_dict['result'] = "true"

        tEla = time.time() - tStart
        print()
        print('Elapsed time (sec.)', round(tEla, 3))

    except Exception as e:
        print('The exception is:', e)
        print("Input is not a valid!")
        raise HTTPException(status_code=415, detail="Unsupported request.")

    return out_dict
#
# delete speaker
#
@app.post("/delete_speaker", tags=["Operation"])
def delete_speaker(name: str):
    global centroids

    log.info("Delete a speaker from DB")

    # create the new_centroids without speaker = name
    # check if name is in speakers list
    list_speakers = get_list_speakers_names(centroids, ordered=False)

    if name in list_speakers:
        # Cancel, operate on a copy
        new_centroids = centroids.copy()
 
        # Remove the speaker from the data structure
        del new_centroids[name]

        # now save
        if config.global_settings['CONFIG_TYPE'] == "cloud":
            log.info("Writing new centroid to oss")
            write_new_centroids_to_oss(new_centroids)
        else:
            # local
            log.info("Writing new centroid to local")
            write_new_centroids_to_local(new_centroids)

        # swap
        log.info("Swap centroids files")
        swap_centroids_files()

        # after creating the new centroids file, reload it
        centroids = load_centroids()
    else:
        # do nothing
        log.info(name + " not in list speakers")

    dict_out = {}
    dict_out["result"] = "true"

    return dict_out
#
# force the reload of the centroids file
#
@app.get("/reload", tags=["Operation"])
def reload():
    global centroids

    centroids = load_centroids()

    out_dict = {}
    out_dict['result'] = "true"

    return out_dict
#
# restore of the centroids file
#
@app.get("/restore_centroids", tags=["Operation"])
def restore_centroids():
    global centroids

    print("Restore centroids")
    restore_centroids_from_bck()

    centroids = load_centroids()

    out_dict = {}
    out_dict['result'] = "true"

    return out_dict

#
# return the list of registered speakers' names reading the file
# the list can be sorted
#
@app.get("/list_speakers_from_newfile", tags=["Operation"])
def list_speakers_from_newfile(ordered: str = "false"):
    
    new_centroids = load_centroids_newfile()

    list_speakers = []

    for key in new_centroids.keys():
        list_speakers.append(key)
    
    if ordered == "true":
        list_speakers = sorted(list_speakers)

    out_dict = {}
    out_dict['speakers'] = list_speakers

    print_dict(out_dict)

    return out_dict

#
# Main
#
if __name__ == '__main__':
    # set IP on which is listening, port
    # listen on all IP
    uvicorn.run(app, host=config.global_settings['IP'], port=config.global_settings['PORT'])

