import pandas as pd
import os
import numpy as np
import datetime
import time

# data = pd.read_csv('full_data.csv')

os.chdir('C:\\Users\\yeachan153\\Desktop\\Joeri\\Project')
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

# 2)
thesis_data = all_courses_excel.parse('JustThesis')
thesis_list = list(set(thesis_data.iloc[:, 4]))

'''
Master DataFrame
1) Add Master Track 
2) Add Thesis Grades [NATALIE]
3) Start date specific (month, year) [DONE]
4) Number of EC's taken [DONE]

1) 2nd dataframe (AFTER MASTER TRACK, per track): mandatory courses columns. Should contain years
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
    sept_mask = (ECD['grade_date'] >= '201{}-09-21'.format(i)) & (ECD['grade_date'] <= '201{}-02-19'.format(i+1))
    sept_start = ECD[sept_mask]['grade_date'] # Only show students who meet criteria above
    sept_start.index # Index of these students
    ECD.loc[sept_start.index,'Start Date'] = '201{}-09-01'.format(i)

    feb_mask = (ECD['grade_date'] >= '201{}-02-20'.format(i+1)) & (ECD['grade_date'] <= '201{}-09-20'.format(i+1))
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




