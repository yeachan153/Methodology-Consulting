import pandas as pd
import os
import numpy as np
from collections import Counter
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
grad_data.rename(columns = {'ID':'StudentID'}, inplace = True)

# 2)
course_data.Grade.replace({'AVV':6,'V':6,'VLD':6,'G':6,'NAVO':4,'NA':4,'NAV':4,
                           'ONW':4, 'VR':np.nan, 'VRY':np.nan,'NAP':np.nan, '-':np.nan,
                           'O':4, '10':10,'6':6,'6,0':6,'6,5':6.5,'7,0':7,'7,5':7.5,'8,0':8,
                           '8,3':8.3,'8,5':8.5,'9,0':9,'9,5':9.5}, inplace = True)

# 3)
course_data['Grade'] = pd.to_numeric(course_data.Grade)

'''
Generating a new CSV containing grades in wide format
# 1) Converting course_data to wide and joining with grad_data
'''

# 1)
course_data['Overdracht'] = course_data.Overdracht.astype(str)
wide_grades = pd.pivot_table(course_data, index = 'StudentID', columns = 'Title Course', values = 'Grade')

wide_grades.to_csv('wide_grades.csv')
wide_grades2 = pd.read_csv('wide_grades.csv')
wide_data = pd.merge(grad_data, wide_grades2,on = 'StudentID')

# 2)
thesis_data = all_courses_excel.parse('JustThesis')
thesis_list = list(set(thesis_data.iloc[:,4]))


'''
Master DataFrame
1) Add Master Track
2) Add Start Date
3) Add Thesis Grades
4) Start year non-specific (year)
5) Start date specific (month, year)
6) Graduation - Start date
7) Number of EC's taken
  
1) 2nd dataframe (AFTER MASTER TRACK, per track): mandatory courses columns. Should contain years
'''











