# Not possible!

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import copy
from datetime import datetime
import itertools
from collections import Counter

def to_strptime(string):
    try:
        return datetime.strptime(string, "%Y-%m-%d")
    except Exception as e:
        print(e)

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')
data = data[data['Description'] == 'M Psychologie']

data['Start Date'] = data['Start Date'].apply(to_strptime)

filter_14 = datetime.strptime('2014-09-01', "%Y-%m-%d")
data = data[data['Start Date'] < filter_14]

# Deducing the mandatory courses
unique_spec = list(set(data['Specialisation']))
unique_spec = list(filter(lambda x: str(x) != 'nan', unique_spec))
dict1 = {}
grouped = data.groupby('Specialisation')

for each_specialisation in unique_spec:
    current_spec = grouped.get_group(each_specialisation)
    dict1[each_specialisation] = Counter()
    for idx, row in current_spec.iterrows():
        courses_taken_grades = row.iloc[14:][row.iloc[14:].notnull()]
        courses_taken = list(set(courses_taken_grades.index))
        for each_course in courses_taken:
            dict1[each_specialisation].update([each_course])


# Post 2014
os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')
data = data[data['Description'] == 'M Psychologie']
data['Start Date'] = data['Start Date'].apply(to_strptime)

filter_14 = datetime.strptime('2014-09-01', "%Y-%m-%d")
data = data[data['Start Date'] >= filter_14]


