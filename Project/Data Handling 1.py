import pandas as pd
import os
import numpy as np
'''
Reading in both datasets:
grad_data = Wide format data on graduation (pre-filtered for Master's Psychology students)

course_data = Long format data on courses
Only Ondw.eenh considered. 
'''
os.chdir('C:\\Users\\yeachan153\\Desktop\\Joeri\\Project')

graduation_data_excel = pd.ExcelFile('Graduation Dates.xls')

# Selected sheet contains what I need
graduation_data_excel.sheet_names
grad_data = graduation_data_excel.parse('Selected')

all_courses_excel = pd.ExcelFile('All results from 2010 - 2017.xlsx')

# Selected sheet contains what I need
all_courses_excel.sheet_names
course_data = all_courses_excel.parse('Selected')

# Third sheet of all_courses
course_data2 = all_courses_excel.parse('Selected2')
'''
Recoding data:
1) Change column of ID in grad_data to StudentID
2) Renaming Grade items in course_data: Check coding in 2nd meeting questions google docs (confirm what 'NAV' and 'O' are). 11 is NaN
3) Switching grade to numeric format
'''
# 1)
grad_data.rename(columns = {'ID':'StudentID'}, inplace = True)

# 2)
course_data.Grade.replace({'AVV':6,'V':6,'VLD':6,'G':6,'NAVO':4,'NA':4,'NAV':4,
                           'ONW':4, 'VR':np.nan, 'VRY':np.nan,'NAP':np.nan, '-':np.nan,
                           'O':4, '10':10,'6':6,'6,0':6,'6,5':6.5,'7,0':7,'7,5':7.5,'8,0':8,
                           '8,3':8.3,'8,5':8.5,'9,0':9,'9,5':9.5}, inplace = True)

course_data2.Grade.replace({'AVV':6,'V':6,'VLD':6,'G':6,'NAVO':4,'NA':4,'NAV':4,
                           'ONW':4, 'VR':np.nan, 'VRY':np.nan,'NAP':np.nan, '-':np.nan,
                           'O':4, '10':10,'6':6,'6,0':6,'6,5':6.5,'7,0':7,'7,5':7.5,'8,0':8,
                           '8,3':8.3,'8,5':8.5,'9,0':9,'9,5':9.5}, inplace = True)

# 3)
course_data['Grade'] = pd.to_numeric(course_data.Grade)
course_data2['Grade'] = pd.to_numeric(course_data2.Grade)

'''
Generating a new CSV containing grades in wide format
!! Note that you should go to excel and delete the first row filled with "grades" and rename first column "StudentID" in order
for the join to work
'''
# 1)
course_data['Overdracht'] = course_data.Overdracht.astype(str)
wide_grades = pd.pivot_table(course_data, index = 'StudentID', columns = ['Title Course'])
# wide_grades.to_csv('all_grades.csv')

'''
Joining all_grades selected sheet and grad_data
'''
wide_grades = pd.read_csv('all_grades.csv')
wide_data = pd.merge(grad_data, wide_grades,on = 'StudentID')
# wide_data.to_csv('full_data.csv', index = False)