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

pre_data = data[data['Start Date'] < filter_14]
post_data = data[data['Start Date'] >= filter_14]

pre_filtercopy = copy.deepcopy(pre_data)
pre_groups = pre_filtercopy.groupby('Specialisation')

# Within each group, select the most popular courses and get their correlations
org = pre_groups.get_group('Spec Work & Organ. Psychology')
soc = pre_groups.get_group('Spec Social Psychology')
sport = pre_groups.get_group('Track Sport & Performance Psy')
gen = pre_groups.get_group('General Psychology')    
train = pre_groups.get_group('Track Training & Development')
brain = pre_groups.get_group('Spec Brain & Cognition')    
forensic = pre_groups.get_group('Track Clinical Forensic Psych')

org_subjs = ['Masterstage A&O','Schr./Onderz./An./Pres']
soc_subjs = ['Masterstage Sociale Psych.', 'Recl.VL&Con', 'Sociale psych. v. emoties', 'TSP2: Interventies']
sport_subjs = ['Onderz. Sport & Prest.Ps.','Talent, Expertise & Creat.','Interv. Sport & Prest.Psy',
                'Verdieping Sport/Prest. Psyc', 'Masterstage Ontw. Psych.']
gen_subjs = ['Collectieve Stagebijeenk.','Praktijkstage Klin. Psy.', 'Pract. Klin.Psychodiagn.']
train_subjs = ['Ontwikk. van Trainingen', 'Trainerspracticum', 'Masterstage Sociale Psych.']
brain_subjs =['Masterstage Brein & Cognitie', 'Adv. Topics Cogn. Neurosc.', 'Psychofarmacologie']
forensi_subjs = ['Praktijkstage Klin. Psy.', 'Collectieve Stagebijeenk.', '3 casussen Psychodiagn.']


org_dfs = []
for each_subj in org_subjs:
    current_df = org[org[each_subj].notnull()]
    org_dfs.append(current_df)

for idx, each_df in enumerate(org_dfs):
    print(org_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[org_subjs[idx]]))

soc_dfs = []
for each_subj in soc_subjs:
    current_df = soc[soc[each_subj].notnull()]
    soc_dfs.append(current_df)

for idx, each_df in enumerate(soc_dfs):
    print(soc_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[soc_subjs[idx]]))

sport_dfs = []
for each_subj in sport_subjs:
    current_df = sport[sport[each_subj].notnull()]
    sport_dfs.append(current_df)

for idx, each_df in enumerate(sport_dfs):
    print(sport_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[sport_subjs[idx]]))

# Graphs to plot!
org = pre_groups.get_group('Spec Work & Organ. Psychology')
soc = pre_groups.get_group('Spec Social Psychology')
sport = pre_groups.get_group('Track Sport & Performance Psy')
gen = pre_groups.get_group('General Psychology')    
train = pre_groups.get_group('Track Training & Development')
brain = pre_groups.get_group('Spec Brain & Cognition')    
forensic = pre_groups.get_group('Track Clinical Forensic Psych')

org_subjs = ['Schr./Onderz./An./Pres']
soc_subjs = ['Masterstage Sociale Psych.', 'TSP2: Interventies']
sport_subjs = ['Masterstage Ontw. Psych.']
gen_subjs = ['Praktijkstage Klin. Psy.']
brain_subjs =['Masterstage Brein & Cognitie']

org_subjs.extend(soc_subjs+sport_subjs+gen_subjs+brain_subjs)
all_subjects = org_subjs

spec = [org, soc,soc,sport,gen,brain]

list_df = [org[org['Schr./Onderz./An./Pres'].notnull()],soc[soc['Masterstage Sociale Psych.'].notnull()],
               soc[soc['TSP2: Interventies'].notnull()],sport[sport['Masterstage Ontw. Psych.'].notnull()],
               gen[gen['Praktijkstage Klin. Psy.'].notnull()],brain[brain['Masterstage Brein & Cognitie'].notnull()]]
               

# For Post 2014
post_filtercopy = copy.deepcopy(post_data)
post_groups = post_filtercopy.groupby('Specialisation')

# Within each group, select the most popular courses and get their correlations
org = post_groups.get_group('Spec Work & Organ. Psychology')
soc = post_groups.get_group('Spec Social Psychology')
sport = post_groups.get_group('Track Sport & Performance Psy')
train = post_groups.get_group('Track Training & Development')

org_subjs = ['Masterstage A&O', 'Conflict en Coöperatie', 'Schr./Onderz./An./Pres', 'Creativiteit in Organisaties',
             'MAPS']
soc_subjs = ['Masterstage Sociale Psych.', 'Emotionele Beïnvloeding', 'Recl.VL&Con', 'Ontwikkelen en Ev. v. Int.',
             'Meting van Attitudes & Gedrag']
sport_subjs = ['Onderz. Sport & Prest.Ps.', 'Talent, Expertise & Creat.','Verdieping Sport/Prest. Psyc', 
               'Interv. Sport & Prest.Psy', 'Masterstage Sport & Prestati']
train_subjs = ['Trainerspracticum', 'Ontwikk. van Trainingen','Masterstage T&D','Literatuuropdracht T&D']

org_dfs = []
for each_subj in org_subjs:
    current_df = org[org[each_subj].notnull()]
    org_dfs.append(current_df)

for idx, each_df in enumerate(org_dfs):
    print(org_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[org_subjs[idx]]))

soc_dfs = []
for each_subj in soc_subjs:
    current_df = soc[soc[each_subj].notnull()]
    soc_dfs.append(current_df)

for idx, each_df in enumerate(soc_dfs):
    print(soc_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[soc_subjs[idx]]))
    
sport_dfs = []
for each_subj in sport_subjs:
    current_df = sport[sport[each_subj].notnull()]
    sport_dfs.append(current_df)

for idx, each_df in enumerate(sport_dfs):
    print(sport_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[sport_subjs[idx]]))
    
train_dfs = []
for each_subj in train_subjs:
    current_df = train[train[each_subj].notnull()]
    train_dfs.append(current_df)

for idx, each_df in enumerate(train_dfs):
    print(train_subjs[idx])
    print(stats.spearmanr(each_df['thesis_grades'], each_df[train_subjs[idx]]))

org = post_groups.get_group('Spec Work & Organ. Psychology')
soc = post_groups.get_group('Spec Social Psychology')
sport = post_groups.get_group('Track Sport & Performance Psy')

org_subjs = ['Masterstage A&O','Conflict en Coöperatie','Schr./Onderz./An./Pres','Creativiteit in Organisaties']
soc_subjs = ['Emotionele Beïnvloeding', 'Recl.VL&Con', 'Ontwikkelen en Ev. v. Int.']
sport_subjs = ['Onderz. Sport & Prest.Ps.','Talent, Expertise & Creat.']
















