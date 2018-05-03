# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:23:14 2018

@author: Ana
"""

import os
import csv
import pandas as pd
from gensim.models import KeyedVectors

# set directory
os.chdir("G:\Mi unidad\UPF")

path_to_files = os.getcwd() + "\data"

# reading data    
proposals = pd.read_csv(path_to_files + "\proposals_actions_lang.csv", sep=",", header=0)

# reading word embeddingn'
word_vectors = KeyedVectors.load(path_to_files + '\wordembeddings\es\es.bin')



weCAT = pd.read_csv(path_to_files + "\wordembeddings\ca.tsv", sep="\t", header=0)

with open(path_to_files + "\wordembeddings\ca.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t")
    for row in rd:
        print(row)


proposals









