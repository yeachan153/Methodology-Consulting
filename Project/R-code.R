library(dplyr)

# TODO (1) THESIS GRADES
data_grades = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/wide_grades.csv")

# 1. extract columns with "Thesis" (coded for Research Masters students) & "these" (other tracks):
thesis_cols = data_grades[,grepl("Thesis", names(data_grades))]
these_cols = data_grades[,grepl("these",  names(data_grades))]

# 2. remove columns with mastertheseCONCEPT & PROPOSAL grade (not actual thesis grades) 
col_names1 = colnames(thesis_cols[, !grepl("Proposal", names(thesis_cols))])
col_names2 = colnames(these_cols[, !grepl("concept", names(these_cols))])

# combine list of col names:
NameList = c(col_names1,col_names2)

# subset new dataframe with studentID and colnames list
thesis_grades = rowSums(data_grades[,colnames(data_grades) %in% NameList], na.rm=TRUE)
studentID_col = data_grades["StudentID"]
thesis_grade_df = cbind(studentID_col, thesis_grades) 

# ISSUES:
    range(thesis_grades) 
    # some thesis_grades > 10; others 0.
    # double check for missing columns (step 1) or columns that should be removed (step 2)
    # ready to inner join (by studentID) in Master Dataframe
