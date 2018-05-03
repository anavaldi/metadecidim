# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 12:54:50 2018

@author: Ana
"""

import os
import pandas as pd
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
import nltk
import nltk.corpus
import stop_words
import re
from scipy.spatial import distance

# Set dir
os.chdir("G:\Mi unidad\UPF")
path_to_files = os.getcwd() + "\data"

# Import dataset
proposals = pd.read_csv(path_to_files + "\proposals_clean.csv", sep=";", header=0)
actions = pd.read_csv(path_to_files + "\\actions_clean.csv", sep=";", header=0)

# Compute average of word2vec of proposals
nltk.download('punkt')
nltk.download('stopwords')
stop_words_ca = stop_words.get_stop_words('catalan')
stop_words_es = stop_words.get_stop_words('spanish')

# import word2vec catalan and spanish
word_vectors_ca = KeyedVectors.load(path_to_files + "\ca.bin") 
word_vectors_ca.wv.vocab

word_vectors_es = KeyedVectors.load(path_to_files + "\es.bin") 
word_vectors_es.wv.vocab

# function which tokenizes words
def tokenize_only(text, lang):
    text = text.decode('utf-8', errors='ignore')
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # take only words
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    # delte stop words
    if lang == 'ca':
        filtered_tokens = [word for word in filtered_tokens if word not in stop_words_ca]
    else:
       filtered_tokens = [word for word in filtered_tokens if word not in stop_words_es]        
    return filtered_tokens

# tokenize_only(proposals.text_ca[1827], 'ca')

# function which computes mean for each word in the doc
def word2vec_mean(text, lang):
    # remove out-of-vocabulary words
    tokens = tokenize_only(text, lang)
    if lang == 'ca':
        word2vec_model = word_vectors_ca
    else:
        word2vec_model = word_vectors_es
    tokens = [word for word in tokens if word in word2vec_model.wv.vocab]
    if len(tokens) > 0:
        return np.mean(word2vec_model[tokens], axis=0)
    else:
        return np.empty(300)       

# word2vec_mean(proposals.text_ca[1200], 'ca')

# computes cos_sim for Catalan and Spanish
doc2vec_proposals_ca = []
doc2vec_actions_ca = []
doc2vec_proposals_es = []
doc2vec_actions_es = []

for index, row in proposals.iterrows():
    print(index)
    doc2vec_proposals_ca.append(word2vec_mean(row['text_ca'], 'ca'))
    doc2vec_proposals_es.append(word2vec_mean(row['text_es'], 'es'))
    
for index, row in actions.iterrows():
    print(index)
    doc2vec_actions_ca.append(word2vec_mean(row['text_ca'], 'ca'))
    doc2vec_actions_es.append(word2vec_mean(row['text_es'], 'es'))

keys = proposals.groupby('action_id').groups.keys()

def cos_sim(a, b):
	""" 2 vectors a, b and returns the cosine similarity according 
	to the definition of the dot product
	"""
	dot_product = np.dot(a, b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	return dot_product / (norm_a * norm_b)


proposals['row_order'] = range(0, len(proposals))
actions['row_order'] = range(0, len(actions))

for index in range(0, len(keys)):
    df = proposals.loc[proposals['action_id'] == keys[index]]
    print(keys[index])    
    for index2, row2 in df.iterrows():
        print index2
        index_v1 = int(actions.loc[actions['action_id'] == keys[index], 'row_order'].values[0])
        index_v2 = int(df.at[index2, 'row_order'])
        v1 = doc2vec_actions_ca[index_v1]
        v2 = doc2vec_proposals_ca[index_v2]
        proposals.loc[proposals['row_order'] == index_v2, 'cos_sim_ca'] = round(distance.cosine(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'eucl_dist_ca'] = round(distance.sqeuclidean(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'mink_dist_ca'] = round(distance.minkowski(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'manh_dist_ca'] = round(distance.cityblock(v1, v2), 2)

        v1 = doc2vec_actions_es[index_v1]
        v2 = doc2vec_proposals_es[index_v2]
        proposals.loc[proposals['row_order'] == index_v2, 'cos_sim_es'] = round(distance.cosine(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'eucl_dist_es'] = round(distance.sqeuclidean(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'mink_dist_es'] = round(distance.minkowski(v1, v2), 2)
        proposals.loc[proposals['row_order'] == index_v2, 'manh_dist_es'] = round(distance.cityblock(v1, v2), 2)

    
    
proposals.to_csv(path_to_files + '\\proposals_actions_similiarity_2.csv', sep=',')
