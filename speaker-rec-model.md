## The Speaker Recognition Model
The technology underlying the Speaker Recognition Service is a Deep Neural Network.

The network, trained on a large dataset of voices, gives us the ability to translate the recording of the voice into a vector in a highly dimensional space of features.

In this way, to identify the speaker in a dataset of registered speakers we need only to compute the distance between vectors. The most probable speaker in the dataset is the closest to the vector of the input voice.

### Supported languages
We have tested the system using **Italian and English** languages. 

Since the recognition is based on features of the human voice (frequencies, tone...) and not on words'recognition it should work mostly independently from the language.

### The theory
The theory underlying the development of the Deep Speaker model is well descibed in arXiv paper: https://arxiv.org/pdf/1705.02304.pdf

### Credits
The Deep Learning model is partially based on the work done by Philippe Remy.

The original code is available in the GitHub repository: https://github.com/philipperemy/deep-speaker

