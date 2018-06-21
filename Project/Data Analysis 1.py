import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')
list(data)[0:12] # Columns

'''
Functions
1) Jitter function
'''
def rand_jitter(arr):
    stdev = .01*(max(arr)-min(arr))
    return arr + np.random.randn(len(arr)) * stdev

'''
ECs taken and thesis grade
1) Seperate into RMes and MSc, check for missing values
2) Remove MSc and RMes students with <60ECs & <120ECs
3) Deal with RMes first
    3a) Check normality of ECs and thesis_grades
    3b) Running spearmans + graph
'''

# 1)
MSc = data[data['Description']=='M Psychologie']
RMes = data[data['Description']=='M Psychology (res)']

set(RMes['EC taken'].isnull())
set(RMes['thesis_grades'].isnull())
set(MSc['EC taken'].isnull())
set(MSc['thesis_grades'].isnull())

# 2)
print(str(MSc.shape[0] - MSc[MSc['EC taken'] >= 60].shape[0]) + ' MSc students removed with <60ECs')
MSc_filtered = MSc[MSc['EC taken'] >= 60]

print(str(RMes.shape[0] - RMes[RMes['EC taken'] >= 120].shape[0]) + ' RMes students removed with <120ECs')
RMes_filtered = RMes[RMes['EC taken'] >= 120]

# 3a) Checking normality
stats.kstest(RMes_filtered['thesis_grades'],'norm')
stats.kstest(RMes_filtered['EC taken'],'norm')
# 3b) Spearmans
stats.spearmanr(RMes_filtered['thesis_grades'], RMes_filtered['EC taken']) # rs = 0.0572, p = 0.520

fig, ax = plt.subplots(figsize = (10,10))
sns.regplot(RMes_filtered['EC taken'], RMes_filtered['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('ECs taken')
plt.ylabel('Thesis Grade')
plt.title('ECs against thesis grade')
sns.set_style('dark')
plt.show()





























