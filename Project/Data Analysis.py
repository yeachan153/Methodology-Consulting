import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import copy

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
4) MSc
    4a) MSc all spec spearman's
    4b) Checking cor & Plotting for specialisations with significant correlations (i.e. Track training & development)
        4bi) 
    4c) Does the correlation for MSc students as a whole remain signficant after removing Training & Development?
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

fig, ax = plt.subplots(figsize = (45,24))
sns.regplot(RMes_filtered['EC taken'], RMes_filtered['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('ECs taken', fontsize = 35)
plt.ylabel('Thesis Grade', fontsize = 35)
plt.title('ECs against thesis grade (RMes)', fontsize = 35)
sns.set_style('darkgrid')
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
ax.set_ylim(5,10.1)
ax.set_xlim(119, 156)
ax.text(145, 5.2, 'rs = 0.0572, p = 0.520, n = 129', fontsize = 50)
plt.show()

# 4a) MSc all spec
stats.kstest(MSc_filtered['thesis_grades'],'norm')
stats.kstest(MSc_filtered['EC taken'],'norm')
stats.spearmanr(MSc_filtered['thesis_grades'], MSc_filtered['EC taken']) # rs = 0.102, p = 0.0046

fig, ax = plt.subplots(figsize = (45,24))
sns.regplot(MSc_filtered['EC taken'], MSc_filtered['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('ECs taken', fontsize = 35)
plt.ylabel('Thesis Grade', fontsize = 35)
plt.title('ECs against thesis grade (MSc)', fontsize = 35)
sns.set_style('darkgrid')
plt.xticks(fontsize = 25)
ax.set_ylim(5,10)
ax.set_xlim(59,123)
plt.yticks(fontsize = 25)
ax.text(103, 5.2, 'rs = 0.102, p = 0.00462, n = 770', fontsize = 50)
plt.show()

# 4b)
# MSc_filtered['Specialisation'].value_counts().sort_values()
MSc_filtercopy = copy.deepcopy(MSc_filtered)
groups = MSc_filtercopy.groupby('Specialisation')
MSc_filtercopy = groups.filter(lambda x: len(x) > 30) # Selecting specialisations with more than 30 people

spec_groups = MSc_filtercopy.groupby('Specialisation')
list_df = [spec_groups.get_group(x) for x in spec_groups.groups]

norm_dict = {}

for i in range(len(list_df)):
    current_df = list_df[i]
    current_spec = "".join(list(set(current_df['Specialisation'])))
    norm_dict[current_spec] = [stats.kstest(current_df['thesis_grades'],'norm')]
    norm_dict[current_spec].append(stats.kstest(current_df['EC taken'],'norm'))
    
cor_dict = {}

for i in range(len(list_df)):
    current_df = list_df[i]
    current_spec = "".join(list(set(current_df['Specialisation'])))
    cor_dict[current_spec] = stats.spearmanr(current_df['thesis_grades'], current_df['EC taken'])

fig, ax = plt.subplots(figsize = (45,24))
sns.regplot(list_df[6]['EC taken'],list_df[6]['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('ECs taken', fontsize = 35)
plt.ylabel('Thesis Grade', fontsize = 35)
plt.title('ECs against thesis grade (Track Training & Development)', fontsize = 35)
sns.set_style('darkgrid')
plt.xticks(fontsize = 25)
ax.set_ylim(5,10)
ax.set_xlim(59,112)
plt.yticks(fontsize = 25)
ax.text(96.5, 5.2, 'rs = 0.297, p = 0.0210, n = 60', fontsize = 50)
plt.show()

# 4c)
filtered = MSc_filtered[MSc_filtered['Specialisation'] != 'Track Training & Development']
stats.spearmanr(filtered['EC taken'], filtered['thesis_grades'])

#########################################################################################################################
os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
data = pd.read_csv('Master Dataframe.csv')
print(list(data)[0:12]) # Columns

MSc = data[data['Description']=='M Psychologie']
RMes = data[data['Description']=='M Psychology (res)']

print(set(RMes['MSc duration'].isnull()))
print(set(RMes['thesis_grades'].isnull()))
print(set(MSc['MSc duration'].isnull()))
print(set(MSc['thesis_grades'].isnull()))

print(str(MSc.shape[0] - MSc[MSc['MSc duration'] >= 200].shape[0]) + ' MSc students removed who finished within 200 days')
MSc_filtered = MSc[MSc['MSc duration'] >= 200]

print(str(RMes.shape[0] - RMes[RMes['MSc duration'] >= 500].shape[0]) + ' RMes students removed who finished within 500 days')
RMes_filtered = RMes[RMes['MSc duration'] >= 500]

print(stats.kstest(RMes_filtered['thesis_grades'],'norm'))
print(stats.kstest(RMes_filtered['MSc duration'],'norm'))

print(len(RMes_filtered))
stats.spearmanr(RMes_filtered['thesis_grades'], RMes_filtered['MSc duration']) # rs = -0.163, p = 0.0250, n = 189

fig, ax = plt.subplots(figsize = (45,24))
sns.regplot(RMes_filtered['MSc duration'], RMes_filtered['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('Duration (Days)', fontsize = 35)
plt.ylabel('Thesis Grade', fontsize = 35)
plt.title('Duration taken against thesis grade (RMes)', fontsize = 35)
sns.set_style('darkgrid')
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
ax.set_ylim(5,10.1)
ax.set_xlim(650, 1300)
ax.text(1100, 5.2, 'rs = -0.163, p = 0.0250, n = 189', fontsize = 50)
plt.show()

print(stats.kstest(MSc_filtered['thesis_grades'],'norm'))
print(stats.kstest(MSc_filtered['MSc duration'],'norm'))

stats.spearmanr(MSc_filtered['thesis_grades'], MSc_filtered['MSc duration']) # rs = -0.178, p < 0.001, n = 865

fig, ax = plt.subplots(figsize = (45,24))
sns.regplot(MSc_filtered['MSc duration'], MSc_filtered['thesis_grades'], color = 'black', y_jitter = 0.05)
plt.xlabel('Duration (Days)', fontsize = 35)
plt.ylabel('Thesis Grade', fontsize = 35)
plt.title('Duration taken against thesis grade (1 Year MSc)', fontsize = 35)
sns.set_style('darkgrid')
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
ax.set_ylim(5,10.1)
ax.set_xlim(150, 1500)
ax.text(1100, 5.2, 'rs = -0.178, p < 0.001, n = 865', fontsize = 50)
plt.show()

MSc_filtered['Specialisation'].value_counts().sort_values(ascending = False)
print(str(MSc_filtered['Specialisation'].value_counts().sum()) + ' out of ' + str(len(MSc_filtered)) +
      ' students have specialisations')


# Selecting specialisations with more than 20 people# Select 

MSc_filtercopy = copy.deepcopy(MSc_filtered)
groups = MSc_filtercopy.groupby('Specialisation')
MSc_filtercopy = groups.filter(lambda x: len(x) > 20) 

print('After selecting specialisations with more than 20 students, we are left with ' + str(len(MSc_filtercopy)) + ' students')
print('We will look at: ' + ", ".join(list(set(MSc_filtercopy['Specialisation']))))

spec_groups = MSc_filtercopy.groupby('Specialisation')
list_df = [spec_groups.get_group(x) for x in spec_groups.groups]

norm_dict = {}

for i in range(len(list_df)):
    current_df = list_df[i]
    current_spec = "".join(list(set(current_df['Specialisation'])))
    norm_dict[current_spec] = [stats.kstest(current_df['thesis_grades'],'norm')]
    norm_dict[current_spec].append(stats.kstest(current_df['MSc duration'],'norm'))

print(norm_dict)

cor_dict = {}

for i in range(len(list_df)):
    current_df = list_df[i]
    current_spec = "".join(list(set(current_df['Specialisation'])))
    cor_dict[current_spec] = stats.spearmanr(current_df['thesis_grades'], current_df['MSc duration'])

cor_dict

# Vertical plots

list_select = [list_df[2], list_df[3], list_df[4]] # Social psych, Work & Org, Behaviour & Health
title = ['Duration taken against thesis grade (Social Psychology)','Duration taken against thesis grade (Work & Organ. Psychology)',
        'Duration taken against thesis grade (Behaviour & Health)']
text = ['rs = -0.255, p < 0.001, n = 189', 'rs = -0.187, p  0.00616, n = 213', 'rs = -0.373, p = 0.00201, n = 66']

fig = plt.figure(figsize = (45,35))
for i in range(3):
    ax = fig.add_subplot(3,1,i+1)
    sns.regplot(list_select[i]['MSc duration'], list_select[i]['thesis_grades'], color = 'black', y_jitter = 0.05)
    sns.set_style('darkgrid')
    ax.set_title(title[i], fontsize = 35)
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    plt.xlabel('Duration (Days)', fontsize = 35)
    plt.ylabel('Thesis Grade', fontsize = 35)
    ax.set_ylim(5,10)
    ax.set_xlim(180,1100)
    if i == 0:
        ax.text(910, 5.2, text[i], fontsize = 35)
    if i == 1:
        ax.text(900, 5.2, text[i], fontsize = 35)
    if i == 2:
        ax.text(900, 5.2, text[i], fontsize = 35)

###########################################################################################################################








































