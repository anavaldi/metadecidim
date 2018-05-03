# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 13:23:14 2018

@author: Ana
"""

import os
import pandas as pd
from langdetect import detect

# set directory
os.chdir("G:\Mi unidad\UPF")

path_to_files = os.getcwd() + "\data"

# reading data    
proposals = pd.read_csv(path_to_files + "\\proposals_actions.csv", sep=",", header=0)

# traductor
proposals = proposals.assign(language = map(lambda x: detect(x.decode("utf-8")), proposals["title_body"]))

proposals['language'].value_counts()

#barlist = proposals['language'].value_counts().plot(kind='bar')
#barlist.set_color(colors=['r', 'g', 'b', 'c'])
#plt.show()

# there exist foreign languages but they are incorrectly detected

# change incorrect language detection
proposals.loc[proposals['language'] == 'pt']
proposals.loc[[36], 'language'] = 'ca'
proposals.loc[[1218], 'language'] = 'ca'
proposals.loc[[1562], 'language'] = 'ca'
proposals.loc[[3216], 'language'] = 'ca'
proposals.loc[[6129], 'language'] = 'es'
proposals.loc[[6130], 'language'] = 'es'

proposals.loc[proposals['language'] == 'nl']
proposals.loc[[3485], 'language'] = 'ca'
proposals.loc[[3486], 'language'] = 'ca'
proposals.loc[[3487], 'language'] = 'ca'
proposals.loc[[3488], 'language'] = 'ca'
proposals.loc[[3783], 'language'] = 'ca'

proposals.loc[proposals['language'] == 'it']
proposals.loc[[3302], 'language'] = 'ca'
proposals.loc[[3420], 'language'] = 'ca'
proposals.loc[[4560], 'language'] = 'ca'
proposals.loc[[5374], 'language'] = 'ca'
proposals.loc[[5839], 'language'] = 'ca'

proposals.loc[proposals['language'] == 'en']
proposals.loc[[1052], 'language'] = 'ca'
proposals.loc[[3437], 'language'] = 'ca'

proposals.loc[proposals['language'] == 'fr']
proposals.loc[[1546], 'language'] = 'ca'
proposals.loc[[3214], 'language'] = 'ca'

proposals['language'].value_counts()

# write final csv
proposals.to_csv(path_to_files + '\\proposals_actions_lang.csv', sep=',')



