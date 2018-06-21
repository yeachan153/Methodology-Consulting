import os
import pandas as pd
import matplotlib.pyplot as plt
os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
list(data)[0:12] # Columns
'''
ECs taken and thesis grade
1) Seperate into RMes and MSc
'''
MSc = data[data['Description']=='M Psychologie']
RMes = data[data['Description']=='M Psychology (res)']



