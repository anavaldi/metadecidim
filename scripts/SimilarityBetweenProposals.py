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

# Set dir
# os.chdir("G:\Mi unidad\UPF")
# path_to_files = os.getcwd() + "\data"

# Import dataset
# proposals = pd.read_csv(path_to_files + "\proposals_actions_lang.csv", sep=",", header=0)
proposals = pd.read_csv("\data\proposals_actions_lang.csv", sep=",", header=0)

# Set some wrong langauge labels by hand
proposals.iloc[2510, proposals.columns.get_loc('language')] = 'ca'
proposals.iloc[3656, proposals.columns.get_loc('language')] = 'ca'
proposals.iloc[5274, proposals.columns.get_loc('language')] = 'ca'

# Import word2vec catalan and spanish
word_vectors_ca = KeyedVectors.load(path_to_files + "\ca.bin") 
word_vectors_ca.wv.vocab

word_vectors_es = KeyedVectors.load(path_to_files + "\es.bin") 
word_vectors_es.wv.vocab

# Delete actions with no 'Ajuntament de Barcelona' as author in any proposals
proposals = proposals.groupby('action_id').filter(lambda df: (df.author_name == 'Ajuntament de Barcelona').any())

# Delete actions with only one proposals
proposals = proposals.groupby('action_id').filter(lambda df: (len(df)) > 1)

# Compute average of word2vec of proposals
nltk.download('punkt')
nltk.download('stopwords')
stop_words_ca = stop_words.get_stop_words('catalan')
stop_words_es = stop_words.get_stop_words('spanish')

def tokenize_only(text, lang):
    text = text.decode('utf-8')
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

# tokenize_only(proposals.title_body[2510], proposals.language[2510])

def word2vec_mean(text, lang):
    # remove out-of-vocabulary words
    tokens = tokenize_only(text, lang)
    if lang == 'ca':
        word2vec_model = word_vectors_ca
    else:
        word2vec_model = word_vectors_es
    tokens = [word for word in tokens if word in word2vec_model.wv.vocab]
    return np.mean(word2vec_model[tokens], axis=0)

# word2vec_mean(proposals.title_body[2510], 'ca')

doc2vec =[]
for index, row in proposals.iterrows():
    print(index)
    doc2vec.append(word2vec_mean(row["title_body"], row["language"]))
    
proposals.cos_sim = ""

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


for index in range(0, len(keys)):
    df = proposals.loc[proposals['action_id'] == keys[index]]
    print(keys[index])    
    for index2, row2 in df.iterrows():
        print index2
        index_v1 = int(df.loc[df['author_id'] == '1', 'row_order'].values[0])
        index_v2 = int(df.at[index2, 'row_order'])
        v1 = doc2vec[index_v1]
        v2 = doc2vec[index_v2]
        proposals.loc[proposals['row_order'] == index_v2, 'cos_sim'] = round(cos_sim(v1, v2), 2)
 
    
proposals.to_csv(path_to_files + '\\proposals_actions_similiarity.csv', sep=',')
