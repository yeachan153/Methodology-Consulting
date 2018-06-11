library(dplyr)
library(xlsx)
install.packages("readxl")
library(readxl)
require(xlsx)
#------------------------------------------------------
# Part 1. THESIS GRADES

data_grades = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/wide_grades.csv")

# 1. extract columns with "Thesis" (coded for Research Masters students) & "these" (other tracks):
    thesis_cols = data_grades[,grepl("Thesis", names(data_grades))]
    these_cols = data_grades[,grepl("these",  names(data_grades))]
    scriptie_cols = data_grades[,grepl("Scriptie", names(data_grades))]
    werkstuk_cols = data_grades[,grepl("Werkstuk", names(data_grades))]
    # any other columns for thesis?

# 2. remove columns with mastertheseCONCEPT & PROPOSAL grade (not actual thesis grades) 
    col_names1 = colnames(thesis_cols[, !grepl("Proposal", names(thesis_cols))])
    col_names2 = colnames(these_cols[, !grepl("concept", names(these_cols))])
    col_names3 = colnames(scriptie_cols)
    col_names4 = colnames(werkstuk_cols)

# 3. combine list of colnames:
    NameList = c(col_names1,col_names2,col_names3,col_names4)

# 4. subset new dataframe with studentID and colnames list
    thesis_grades = rowSums(data_grades[,colnames(data_grades) %in% NameList], na.rm=TRUE)
    studentID_col = data_grades["StudentID"] # should be the OK bc same index in data_grades
    thesis_grade_df = cbind(studentID_col, thesis_grades) 
    thesis_grade_df[thesis_grades < 10]

# Issues:
    range(thesis_grades) 
    thesis_grade_df[thesis_grade_df$thesis_grades > 10,] 
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades == 0,] )
    # 20 students with > 10 thesis grades and some students = 0

#------------------------------------------------------
# create csv file for studentID and thesis grade table 
    setwd("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project") 
    write.csv(thesis_grade_df, file = "Thesis_Grades.csv",row.names = FALSE)

#------------------------------------------------------
# Adding thesis grade to Master Dataframe.xlsx file:
    master_df = read_xlsx("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/Master Dataframe.xlsx", sheet = "Unfiltered")
    merged_df = merge(x = master_df, y = thesis_grade_df, by = 'StudentID', all.x = TRUE)
    write.csv(thesis_grade_df, file = "merged_thesis.csv")

#-------------------------------------------------------------
# Part 2. CORRELATIONS FOR EACH COURSE AGAINST THESIS GRADES
    
    #data <- as.data.frame(matrix(data = sample(c(1:10),100, replace = TRUE),ncol = 10, nrow = 10))
    data = merged_df[,c(1,11:length(merged_df))]
    correlations <- rep(NA, (length(data[1,])-2))
    a = length(data[1,])-2
    size <- rep(NA, (length(data[1,])-2) )
    for (i in 1:a){
        correlations[i] <- cor(data[,i+1],data[,length(data)], use = "pairwise.complete.obs")
    }
    for (i in 1:a){
        size[i] <- cor.test(data[,i+1],data[,length(data)])$parameter + 2
    }    
    cor.m <- data.frame(names(data[,2:(a+1)]))
    cor.m$cor <- correlations
    cor.m$sample <- size
    
    # rows with correlations higher than 0.5
    cor.m[which(cor.m[,2]>0.5),1]
    
    length(which(cor.m[,2]>0.5)) # 37 courses (including thesis columns ATM)
