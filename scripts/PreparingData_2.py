# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 15:53:35 2018

@author: Ana
"""

import os
import pandas as pd
import numpy as np


# set directory
os.chdir("G:\Mi unidad\UPF")

path_to_files = os.getcwd() + "\data"

# reading data    
proposals = pd.read_csv(path_to_files + '\\proposals_full_result.csv', sep=",", header=0)
actions = pd.read_csv(path_to_files + '\\actions.csv', sep=",")


print(proposals.columns)
print(actions.columns)


# add aciton_id to proposals
actions_aux = actions[['result_id', 'proposal_ids']]
actions_aux[['proposal_ids']] = actions_aux[['proposal_ids']].astype(str)
actions_aux_2 = pd.concat([pd.Series(row['result_id'], row['proposal_ids'].split(';')) for _, row in actions_aux.iterrows()]).reset_index()
actions_aux_2 = actions_aux_2.dropna()
actions_aux_2.columns = ['Proposal ID', 'action__id']      
            
proposals[['Proposal ID']] = proposals[['Proposal ID']].astype(str)
proposals_2 = pd.merge(proposals, actions_aux_2)      
proposals_2.columns = ['id', 'origin', 'scope', 'district', 'category', 
                       'subcategory', 'title', 'description', 'author_id', 
                       'author_name', 'created_at', 'votes', 'comments', 
                       'url', 'status', 'description_es', 'description_ca', 
                       'title_es', 'title_ca', 'action_id']

del proposals, actions_aux, actions_aux_2

# some changes in actions dataset
actions = actions.rename(columns = {'result_id':'action_id'})
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<p>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</p>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<b>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</b>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<div>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</div>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<ul>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</ul>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<li>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</li>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<strong>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('</strong>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('<br>', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('&nbsp', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('\r', '')
actions['title_ca'] = actions['title_ca'].astype(str).str.replace('\n-', '')

actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<p>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</p>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<b>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</b>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<div>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</div>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<ul>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</ul>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<li>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</li>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<strong>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('</strong>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('<br>', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('&nbsp', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('\r', '')
actions['description_ca'] = actions['description_ca'].astype(str).str.replace('\n-', '')

actions['title_es'] = actions['title_es'].astype(str).str.replace('<p>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</p>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<b>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</b>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<div>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</div>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<ul>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</ul>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<li>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</li>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<strong>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('</strong>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('<br>', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('&nbsp', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('\r', '')
actions['title_es'] = actions['title_es'].astype(str).str.replace('\n-', '')

actions['description_es'] = actions['description_es'].astype(str).str.replace('<p>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</p>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<b>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</b>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<div>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</div>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<ul>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</ul>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<li>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</li>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<strong>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('</strong>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('<br>', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('&nbsp', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('\r', '')
actions['description_es'] = actions['description_es'].astype(str).str.replace('\n-', '')

# merge title and body
proposals_2 = proposals_2.assign(text_ca = proposals_2.title_ca + '. ' + proposals_2.description_ca)
proposals_2.text_ca = proposals_2.text_ca.replace('.. ', '. ')

proposals_2 = proposals_2.assign(text_es = proposals_2.title_es + '. ' + proposals_2.description_es)
proposals_2.text_es = proposals_2.text_es.replace('.. ', '. ')

actions = actions.assign(text_ca = actions.title_ca + '. ' + actions.description_ca)
actions.text_ca = actions.text_ca.replace('.. ', '. ')

actions = actions.assign(text_es = actions.title_es + '. ' + actions.description_es)
actions.text_es = actions.text_es.replace('.. ', '. ')

# write final csv
proposals_2.to_csv(path_to_files + '\\proposals_clean.csv', sep=';')
actions.to_csv(path_to_files + '\\actions_clean.csv', sep=';')
