'''
Remove filters

'''
import pandas as pd
import os
import numpy as np
import datetime
import time
from collections import Counter
os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')
import cos2

# wide_data = original master dataframe
# wide_data2 = master dataframe with extra filters and 4 bachelor courses
# wide_data3 = master dataframe with no filters and 4 bachelor courses

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project')

# data = pd.read_csv('full_data.csv')
graduation_data_excel = pd.ExcelFile('Graduation Dates.xls')
# Selected sheet contains what I need
graduation_data_excel.sheet_names
grad_data = graduation_data_excel.parse('Selected')
all_courses_excel = pd.ExcelFile('All results from 2010 - 2017 V2.xlsx')
# Selected sheet contains what I need
all_courses_excel.sheet_names
course_data = all_courses_excel.parse('Selected')
# Third sheet of all_courses


'''
Recoding data:
1) Change column of ID in grad_data to StudentID
2) Renaming Grade items in course_data: Check coding in 2nd meeting questions google docs (confirm what 'NAV' and 'O' are).
3) Switching grade to numeric format
'''
# 1)
grad_data.rename(columns={'ID': 'StudentID'}, inplace=True)

# 2)
course_data.Grade.replace({'AVV': 6, 'V': 6, 'VLD': 6, 'G': 6, 'NAVO': 4, 'NA': 4, 'NAV': 4,
                           'ONW': 4, 'VR': np.nan, 'VRY': np.nan, 'NAP': np.nan, '-': np.nan,
                           'O': 4, '10': 10, '6': 6, '6,0': 6, '6,5': 6.5, '7,0': 7, '7,5': 7.5, '8,0': 8,
                           '8,3': 8.3, '8,5': 8.5, '9,0': 9, '9,5': 9.5}, inplace=True)


# 3)
course_data['Grade'] = pd.to_numeric(course_data.Grade)

'''
Generating a new CSV containing grades in wide format
# 1) Converting course_data to wide and joining with grad_data
'''

# 1)
course_data['Overdracht'] = course_data.Overdracht.astype(str)
wide_grades = pd.pivot_table(course_data, index='StudentID', columns='Title Course', values='Grade')

# wide_grades.to_csv('wide_grades.csv')
wide_grades2 = pd.read_csv('wide_grades.csv')
wide_data = pd.merge(grad_data, wide_grades2, on='StudentID')

'''
Master DataFrame
1) Add Master Track [YEACHAN]
2) Thesis topic
2) Add Thesis Grades [NATALIE]
3) Start date specific (month, year) [DONE]
4) Number of EC's taken [DONE]
5) Master Length [DONE]
6) Adding bachelor data
7) Merging thesis grades
8) Adding specialisation
9) Classifying missing master track for 1 year MSc students using cosine similarity
10) Join:
    - 'Track Training & Development' & 'Track Training and Development' & 'Training & Development'
    - 'Spec Brain & Cognition' & 'Spec B&C, route Cogn Neurosc'
    - 'Spec W&O, route WHP' & 'Spec Work & Organ. Psychology' & 'Work & Organisational Psych'
'''

# 4)
course_data['Overdracht'] = course_data['Overdracht'].astype(float)
EC_wide = pd.pivot_table(course_data, index='StudentID', columns='Title Course', values='Overdracht')
# EC_wide.to_csv('EC_wide.csv')
EC_wide = pd.read_csv('EC_wide.csv')
EC_data_wide = pd.merge(grad_data, EC_wide, on='StudentID')
# Check if indexes match
set(EC_data_wide.index == wide_data.index)
wide_data['EC taken'] = EC_data_wide.iloc[:,7:].apply(np.sum,axis = 1)
# Changing column order
colnames = list(wide_data)
EC = colnames.pop()
colnames.insert(4,EC)
wide_data  = wide_data[colnames]
# wide_data.to_csv('Master Dataframe.csv', index = False)

# 3) 
def to_unix(timestamp):
    try:
        return time.mktime(timestamp.timetuple())
    except Exception as e:
        print(e)

def to_date(unix_float):
    try:
        return datetime.datetime.fromtimestamp(unix_float).strftime('%d/%m/%Y')
    except Exception as e:
        print(e)

def to_strptime(string):
    try:
        return datetime.datetime.strptime(string, "%d/%m/%Y")
    except Exception as e:
        print(e)
        
course_data['unix'] = course_data['Grade date'].apply(to_unix)
colnames = list(course_data)
unix = colnames.pop()
colnames.insert(2,unix)
course_data  = course_data[colnames]

course_start = pd.pivot_table(course_data, index='StudentID', columns='Title Course', values='unix')
earliest_course = course_start.apply(np.min,1)
earliest_course_date = earliest_course.apply(to_date)
ECD = pd.DataFrame(earliest_course_date, columns = ['grade_date'])
ECD['grade_date'] = ECD['grade_date'].apply(to_strptime)

# IF first grad date is 21/09 - 19/02: September start. Else if first grade date is 20/02 - 20/09 
ECD['Start Date'] = None
for i in range(8):
    sept_mask = (ECD['grade_date'] >= '201{}-09-21'.format(i)) & (ECD['grade_date'] <= '201{}-03-01'.format(i+1))
    sept_start = ECD[sept_mask]['grade_date'] # Only show students who meet criteria above
    sept_start.index # Index of these students
    ECD.loc[sept_start.index,'Start Date'] = '201{}-09-01'.format(i)

    feb_mask = (ECD['grade_date'] >= '201{}-03-02'.format(i+1)) & (ECD['grade_date'] <= '201{}-09-20'.format(i+1))
    feb_start = ECD[feb_mask]['grade_date']
    ECD.loc[feb_start.index, 'Start Date'] = '201{}-02-01'.format(i+1)

sept2010_mask = ECD['Start Date'].isnull()
ECD.loc[sept2010_mask, 'Start Date'] = '2010-09-01'

wide_data = pd.merge(wide_data, ECD['Start Date'].to_frame(),  left_on = 'StudentID', right_index = True)
colnames = list(wide_data)
start_date_col = colnames.pop()
colnames.insert(5, start_date_col)
wide_data = wide_data[colnames]

# wide_data.to_csv('Master Dataframe.csv', index = False)

# 5) 
def to_strptime2(string):
    try:
        return datetime.datetime.strptime(string, "%Y-%m-%d")
    except Exception as e:
        print(e)

wide_data['Start Date'] = wide_data['Start Date'].apply(to_strptime2)
wide_data['MSc duration'] = wide_data['Graduation date'] - wide_data['Start Date']
colnames = list(wide_data)
MSc_duration = colnames.pop()
colnames.insert(7, MSc_duration)
wide_data = wide_data[colnames]
wide_data['MSc duration'] = wide_data['MSc duration'].dt.days

# wide_data.to_csv('Master Dataframe.csv', index = False)

# 6)
# Merging bachelor data
bachelor_data = all_courses_excel.parse('Bachelors')

bachelor_data.Grade.replace({'AVV': 6, 'V': 6, 'VLD': 6, 'G': 6, 'NAVO': 4, 'NA': 4, 'NAV': 4,
                           'ONW': 4, 'VR': np.nan, 'VRY': np.nan, 'NAP': np.nan, '-': np.nan,
                           'O': 4, '10': 10, '6': 6, '6,0': 6, '6,5': 6.5, '7,0': 7, '7,5': 7.5, '8,0': 8,
                           '8,3': 8.3, '8,5': 8.5, '9,0': 9, '9,5': 9.5}, inplace=True)
    
bachelor_data['Grade'] = pd.to_numeric(bachelor_data.Grade)
wide_bachelor_grades = pd.pivot_table(bachelor_data, index = 'StudentID', columns = 'Title Course', values = 'Grade')
# wide_bachelor_grades.to_csv('wide_bachelor_grades.csv')
wide_bachelor_grades = pd.read_csv('wide_bachelor_grades.csv')

wide_bachelor_grades['Wetens. en Stat. Redeneren'] = wide_bachelor_grades['Wetens. en Stat. Redeneren'].fillna(wide_bachelor_grades['Wetensch. & Stat. Redeneren'])
wide_bachelor_grades.drop('Wetensch. & Stat. Redeneren', axis = 1, inplace  = True)

wide_data3 = pd.merge(wide_data, wide_bachelor_grades, left_on = 'StudentID', right_on = 'StudentID', how = 'left')
cols = list(wide_data3)[:-3]
last_cols = list(wide_data3)[-3:]

for idx, each_subj in enumerate(last_cols):
    cols.insert(10 + idx, each_subj)

wide_data3 = wide_data3[cols]

# wide_data3.to_csv('Master Dataframe.csv', index = False)

# 7)
thesis_grade = pd.read_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Thesis_Grades.csv')
wide_data3 = pd.merge(wide_data3, thesis_grade, left_on = 'StudentID', right_on = 'StudentID', how = 'left')
col = list(wide_data3)
last = col.pop()
col.insert(8,last)
wide_data3 = wide_data3[col]

# 8)
sp_data = pd.read_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\specialisation2.csv')
sp_data = sp_data[['ID', 'Subplanomschrijving']]
sp_data['Subplanomschrijving'].isnull().sum()
sp_data = sp_data.dropna()
sp_data.rename(columns = {'Subplanomschrijving': 'Specialisation', 'ID':'StudentID'}, inplace = True)
sp_data.reset_index(inplace = True, drop = True)
sp_data.drop_duplicates(subset = 'StudentID', inplace = True)

wide_data3 = pd.merge(wide_data3, sp_data, left_on = 'StudentID', right_on = 'StudentID', how = 'left')
wide_data3[wide_data3['StudentID'].duplicated()] # Row 52 is duplaicted
wide_data3.drop(wide_data3.index[52], inplace = True)

cols = list(wide_data3)
last_col = cols.pop()
cols.insert(8, last_col)
wide_data3 = wide_data3[cols]
wide_data3.head(2)

# wide_data3.to_csv('Master Dataframe Unfiltered.csv', index = False)

# 9)
missing_spec = wide_data3[(wide_data3['Description'] == 'M Psychologie') & (wide_data3['Specialisation'].isnull())]
full_spec =  wide_data3[(wide_data3['Description'] == 'M Psychologie') & (wide_data3['Specialisation'].notnull())]

# Dictionary containing all subjects per mastertrack
dict1 = {}
specialisations = list(set(full_spec['Specialisation']))
for spec in specialisations:
    dict1[spec] = []

for row_number in range(len(full_spec)):
    if full_spec.iloc[row_number, 8] in dict1.keys():
        key = full_spec.iloc[row_number, 8]
        dict1[key].extend([list(full_spec)[idx] for idx, each in enumerate(full_spec.iloc[row_number,:])  if idx > 15 if pd.notnull(each)])

# Find unique subjects per specialisation - join ','
keys = dict1.keys()
for each_key in keys:
    dict1[each_key] = ','.join((set(dict1[each_key])))

'''
# Counting most common specialisations
counter = Counter()
for each in full_spec['Specialisation']:
    if each not in counter:
        counter[each] = 1
    elif each in counter:
        counter.update([each])
'''
os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Cosine similarity\\Train')

# Writing key as filename and value as text
for key,value in dict1.items():
    f = open(key+'.txt',"w")
    f.write(value)
    f.close()

# Creating a corpus like dictionary
corpus2 = {}
for key, value in dict1.items():
    corpus2[key] = {'filename':key+'.txt'}

unique_subjects = Counter()
for docid, info in corpus2.items():
    unique_subjects.update(cos2.get_file_freqs(info['filename']))

print('Number of unique subjects in full spec data:', len(unique_subjects))

common_words_and_values = unique_subjects.most_common()
vocabulary = [each_tuple[0] for each_tuple in common_words_and_values]

docid = [docid for docid, idx in corpus2.items()]
file_names = [corpus2[key]['filename'] for key in corpus2]

for i in range(len(docid)):
    corpus2[docid[i]]['freq_vect'] = cos2.freqs_to_vector(cos2.get_file_freqs(file_names[i]), vocabulary)

# Outputting missing specialisation as .txt
missing_dict = {}

for idx, row in enumerate(missing_spec.iterrows()):
    row = row[1][15:]
    missing_dict[idx] = ','.join(list(row[row.notnull()].index))

os.chdir('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Cosine similarity\\Test')
for key, value in missing_dict.items():
    f = open(str(key)+'.txt', 'w')
    f.write(value)
    f.close()

classifier_list = []
for idx in range(len(missing_dict)):
    a,b = cos2.rank_documents(cos2.text_to_vector(missing_dict[idx], vocabulary), corpus2, num = 2)
    if (b[0] > 0.45):
        classifier_list.append(a[0])
    else:
        classifier_list.append(None)

print(str(pd.notnull(classifier_list).sum() / len(classifier_list) * 100)+'%' + ' of missing values were classified')        

missing_spec.reset_index(inplace = True, drop = True)
missing_spec.loc[:,'Specialisation'] = pd.Series(classifier_list)

full_spec.to_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Cosine similarity\\Data\\full_spec.csv', index = False)
missing_spec.to_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Cosine similarity\\Data\\missing_spec.csv', index = False)

# Joining with RMes data
MSc_data = pd.concat([full_spec,missing_spec], ignore_index = True)
MSc_data['Specialisation'].notnull().sum()/len(MSc_data)

RMes = wide_data3[wide_data3['Description'] == 'M Psychology (res)']
wide_data3 = pd.concat([MSc_data, RMes], ignore_index = True)

wide_data3_filter = wide_data3[(wide_data3['thesis_grades'] <= 10) & (wide_data3['thesis_grades'] > 0)]
print(str(wide_data3.shape[0] - wide_data3_filter.shape[0]) + ' people filtered out with thesis grade = 0 or above 10')

# wide_data3_filter.to_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Master Dataframe.csv', index = False)

# 10)
wide_data3_filter['Specialisation'].replace({'Track Training and Development':'Track Training & Development',
          'Training & Development':'Track Training & Development', 'Spec B&C, route Cogn Neurosc':'Spec Brain & Cognition',
          'Spec W&O, route WHP':'Spec Work & Organ. Psychology', 'Work & Organisational Psych':'Spec Work & Organ. Psychology',
          'Brain and Cognition':'Spec Brain & Cognition' },
    inplace = True)

# wide_data3_filter.to_csv('C:\\Users\\yeachan153\\Desktop\\Methodology-Consulting\\Project\\Master Dataframe.csv', index = False)





















