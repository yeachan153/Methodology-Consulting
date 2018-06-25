import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import copy
import datetime

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')

def to_strptime(string):
    try:
        return datetime.datetime.strptime(string, "%Y-%m-%d")
    except Exception as e:
        print(e)
        
data['Start Date'] = data['Start Date'].apply(to_strptime)
filter_14 = datetime.datetime.strptime('2014-09-01', "%Y-%m-%d")
pre_data = data[data['Start Date'] < filter_14]
post_data = data[data['Start Date'] >= filter_14]

learning = list(data)[12:15]
print(learning)


# Post 2014- All learning courses available
post0 = post_data[post_data[learning[0]].notnull()]
post1 = post_data[post_data[learning[1]].notnull()]
post2 = post_data[post_data[learning[2]].notnull()]

# Pre 2014- Only learning course 'Wetens. en Stat. Redeneren' available
pre2 = pre_data[pre_data[learning[1]].notnull()]

# Correlating:



