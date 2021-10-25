## The Speaker Recognition Model
The technology underlying the Speaker Recognition Service is a Deep Neural Network.

The network, trained on a large dataset of voices, gives us the ability to translate the recording of the voice into a vector in a highly dimensional space of features.

In this way, to identify the speaker in a dataset of registered speakers we need only to compute the distance between vectors. The most probable speaker in the dataset is the closest to the vector of the input voice.

### Siamese Networks
The central idea of the Deep Learning model is to have a NN that has in input the audio clip (preprocessed, as we describe below) and the network produces in output a vector in a 512-dimenaionl space.
These vectors can be used to compute the distance between two audio clips and decide if they belongs to the same speaker or not.
BUt, the network must learn to properly produce these vectors: we want that vectors produced by audio clip of the same speaker are "close" and vectors from different speakers are more distant.
For these, as in most face recognition systems, a Siamese Network is used, with a so called "triplet loss".

In short, for the training of the NN, starting from the train dataset, a series of tripets are assembles (A, P, N). A is the so-called anchor, P is an audio clip from the same speaker of A and N is from a different speaker.

We want to minimize the following Loss Fucntion

triplet loss = max (d(a, p) - d(a, n) +M, 0)


 
### The theory
The theory underlying the development of the Deep Speaker model is well described in arXiv paper: https://arxiv.org/pdf/1705.02304.pdf

### Supported languages
We have tested the system using **Italian and English** languages. 

Since the recognition is based on features of the human voice (frequencies, tone...) and not on words'recognition it should work mostly independently from the language.

### The theory
The theory underlying the development of the Deep Speaker model is well described in arXiv paper: https://arxiv.org/pdf/1705.02304.pdf

### Credits
The Deep Learning model is partially based on the work done by Philippe Remy.

The original code is available in the GitHub repository: https://github.com/philipperemy/deep-speaker

