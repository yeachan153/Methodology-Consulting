import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def to_strptime(string):
    try:
        return datetime.strptime(string, "%Y-%m-%d")
    except Exception as e:
        print(e)

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')

data['Start Date'] = data['Start Date'].apply(to_strptime)

filter_14 = datetime.strptime('2014-09-01', "%Y-%m-%d")

pre_data = data[data['Start Date'] < filter_14]
post_data = data[data['Start Date'] >= filter_14]


