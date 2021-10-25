#
# do some analisys on the centroids data structure
#
import pandas as pd
import numpy as np

from utilities import load_centroids_from_local, distance_cosine_similarity
import config

#
# main
#
centroids = load_centroids_from_local()

list_speakers = sorted(centroids.keys())

print('This is the list of speakers:' , list_speakers)

df = pd.DataFrame(columns=list_speakers)

for i, key1 in enumerate(list_speakers):
    list_dist = []
    for key2 in list_speakers:
        v1 = centroids[key1]
        v2 = centroids[key2]

        dist = round(distance_cosine_similarity(v1, v2)[0], 3)

        list_dist.append(dist)
    
    # reshape to add to df2
    list_dist = np.array(list_dist).reshape((1,9))
    
    df2 = pd.DataFrame(list_dist, columns=list_speakers, index = [key1])
    
    df = df.append(df2)

print(df.head(10))



