# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 13:31:35 2018

@author: Ana
"""
import os
import pandas as pd
import numpy as np


# set directory
os.chdir("G:\Mi unidad\UPF")

path_to_files = os.getcwd() + "\data"

# reading data    
proposals = pd.read_csv(path_to_files + '\\proposals-31-01-2018-42888.csv', sep=";", header=0)
proposals_old = pd.read_csv(path_to_files + '\\proposals.tsv', sep="\t", header=0)
actions = pd.read_csv(path_to_files + '\\actions.csv', sep=",")

print(proposals.columns)
print(proposals.dtypes)

print(proposals_old.columns)
print(proposals_old.dtypes)

print(actions.columns)
print(actions.dtypes)

 # setting columns
proposals['id'] = proposals['id'].astype('object')
proposals['category/id'] = proposals['category/id'].astype('object')
proposals['scope/id'] = proposals['scope/id'].astype('object')
proposals['feature/id'] = proposals['feature/id'].astype('object')

proposals_old['id'] = proposals_old['id'].astype('object')
proposals_old['category__id'] = proposals_old['category__id'].astype('object')

actions['result_id'] = actions['result_id'].astype('object')
actions['decidim_category_id'] = actions['decidim_category_id'].astype('object')
actions['decidim_scope_id'] = actions['decidim_scope_id'].astype('object')
actions['parent_id'] = actions['parent_id'].astype('object')
actions['external_id'] = actions['external_id'].astype('object')
actions['decidim_accountability_status_id'] = actions['decidim_accountability_status_id'].astype('object')
actions['proposal_ids'] = actions['proposal_ids'].astype('object')

# merging columns from proposals_old to proposals (proposals_merge)
proposals_old_aux = (proposals_old[['id', 'author__id', 'author__name', 'source', 'category__id', 
                                   'category__name', 'subcategory__id', 'subcategory__name',
                                   'district__id', 'district__name']])

proposals_aux = proposals[['id', 'title', 'body', 'votes', 'comments']]

proposals_merge = pd.merge(proposals_old_aux, proposals_aux)

proposals_merge = proposals_merge.assign(title_body = proposals_merge.title + '. ' + proposals_merge.body)

del proposals_old_aux, proposals_aux, 
del proposals, proposals_old


# group title+body
proposals_merge.title_body = proposals_merge.title_body.replace('.. ', '. ')
proposals_merge['id'] = proposals_merge['id'].astype('object')

# create cluster variable
actions_aux = actions[['result_id', 'proposal_ids']]
actions_aux[['proposal_ids']] = actions_aux[['proposal_ids']].astype(str)
actions_aux_2 = pd.concat([pd.Series(row['result_id'], row['proposal_ids'].split(';')) for _, row in actions_aux.iterrows()]).reset_index()
actions_aux_2 = actions_aux_2.dropna()
actions_aux_2.columns = ['id', 'action__id']      
            
proposals_merge[['id']] = proposals_merge[['id']].astype(str)
proposals_actions = pd.merge(proposals_merge, actions_aux_2)    
proposals_actions[['id']] = proposals_actions[['id']].astype(int)     
proposals_actions.columns = ['id', 'author_id', 'author_name', 'source', 'category_id',
                             'category_name', 'subcategory_id', 'subcategory_name',
                             'district_id', 'district_name', 'title', 'body', 
                             'votes', 'comments', 'title_body', 'action_id']
        
# write final csv
proposals_actions.to_csv(path_to_files + '\\proposals_actions.csv', sep=';')

















