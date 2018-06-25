import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import copy
from datetime import datetime

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')

# Splitting the data to pre-post 2014
datetime.strptime(data['Start Date'])

list(set(data['Specialisation']))

grouped = data.groupby('Specialisation')
grouped.get_group('Spec Brain & Cognition')
