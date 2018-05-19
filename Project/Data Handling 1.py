import pandas as pd
import os
'''
Reading in both datasets
'''
os.chdir('C:\\Users\\yeachan153\\Desktop\\Joeri\\Project')

graduation_data_excel = pd.ExcelFile('Graduation Dates.xls')

# Selected sheet contains what I need
graduation_data_excel.sheet_names
grad_data = graduation_data_excel.parse('Selected')
set(grad_data['Studieniveau'])

all_courses_excel = pd.ExcelFile('All results from 2010 - 2017 (1).xlsx')

graduation_data = graduation_data_excel.parse('sheet1')
all_courses = all_courses_excel.parse('sheet1')

'''
Changing AllResults from long to wide format
'''
import copy
all_courses_copy = copy.deepcopy(all_courses)

all_courses_copy = all_courses_copy.pivot(list(all_courses_copy))

'''
Joining all courses to graduation data
'''
# Changing ID to StudentID in graduation data before merging
graduation_data.rename(columns = {list(graduation_data)[0]:list(all_courses)[0]}, inplace = True)

