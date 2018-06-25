#install.packages("readxl")
library(dplyr)
library(readxl)
install.packages(c("tidyr","devtools"))
library(tidyr)
library(devtools)
library(dplyr)
library(lattice)
#------------------------------------------------------
# Part 1. THESIS GRADES
rm(list=ls())

data_grades = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/Master Dataframe.csv")

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
    NameList = NameList[-7] # delete "Propedeusethese" 

# 4. subset new dataframe with studentID and colnames list
    subset_df = subset(data_grades, select = c("StudentID", NameList)) # dataframe subset with only student id and thesis modules
    thesis_grades = rowSums(data_grades[,colnames(data_grades) %in% NameList], na.rm=TRUE) 
    studentID_col = data_grades["StudentID"] # should be the OK bc same index in data_grades
    thesis_grade_df = cbind(studentID_col, thesis_grades) 
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades > 10,])

    # Issues:
    range(thesis_grades) 
    thesis_grade_df[thesis_grade_df$thesis_grades > 10,] 
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades > 10,]) #10
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades == 0,]) # 62
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades == 10,]) # 3
    
#------------------------------------------------------
# create csv file for studentID and thesis grade table 
    setwd("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project") 
    #write.csv(thesis_grade_df, file = "Thesis_Grades.csv",row.names = FALSE)

#------------------------------------------------------
# Adding thesis grade to Master Dataframe.xlsx file:
    #master_df = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/Master Dataframe.csv")
    #merged_df = merge(x = master_df, y = thesis_grade_df, by = 'StudentID', all.x = TRUE)
    #write.csv(thesis_grade_df, file = "merged_thesis.csv")

#-------------------------------------------------------------
# Part 2. CORRELATIONS FOR EACH COURSE AGAINST THESIS GRADES
    data = data_grades%>%select(-thesis_grades,thesis_grades) #thesis_grade at the end of the df
    data = data[,c(1,12:length(data))]
    head(data)
    
    # some columns only have NAs or < 3 values; we should exclude these columsn because cor.test() doesn't work for these columns
    data1 = data[,colSums(is.na(data)) < 1098] # since we have 1101 nrows - at least 3 of it should not be NA
    ncol(data1) # data1 excludes 56 courses
    
    a = length(data1[1,])-2
    correlations = rep(NA, (length(data1[1,])-2))
    size = rep(NA, (length(data1[1,])-2) )
    p_value = rep(NA, (length(data1[1,])-2) )
    
    # correlations:
    for (i in 1:a){
        correlations[i] = cor(data1[,i+1],data1$thesis_grades, use = "pairwise.complete.obs", method="spearman")
    }
    #sample size:
    for(i in 1:a){
        size[i]= cor.test((data1[,i + 1]), data1$thesis_grades)$parameter + 2
    }
    #p-value
    for (i in 1:a){
        p_value[i] = cor.test(data1[, i+1], data1$thesis_grades)$p.value
    }
    
    cor_matrix = data.frame(names(data1[,2:(a+1)]))
    cor_matrix$cor = correlations
    cor_matrix$sample = size
    cor_matrix$p.value = p_value
    cor_matrix
    
    # use cor_matrix with sample > 15 
    cor_matrix1 = subset(cor_matrix, cor_matrix$sample > 15)
    # correlation higher than .5:
    cor_matrix2 = subset(cor_matrix1, cor_matrix1$cor >= .5)
    names(cor_matrix2) = c("course_name","cor","sample","p.value") # rename colnames
    cor_matrix3 = cor_matrix2[!grepl("Thesis", cor_matrix2$course_name),] #exclude thesis columns
    cor_matrix4 = cor_matrix3[!grepl("these", cor_matrix3$course_name),]  #exclude these columns
    
    cor_table_output = cor_matrix4[order(cor_matrix4$cor, decreasing=TRUE),]
    write.csv(cor_table_output, file = "Correlation_Msc.csv",row.names = FALSE)
    nrow(cor_matrix4) # 15 courses with correlation > 0.5 & sample > 15  (all sig p.values)

#----------------------------------------------------------------
# correlation between bachelor grades in interested courses and masters thesis grades
    cor_matrix
    # learning course 1: Pract..Onderzoek...Rapp. 
    plot(data$Pract..Onderzoek...Rapp., data$thesis_grades)
    abline(lm(data$thesis_grades ~ data$Pract..Onderzoek...Rapp.), col="blue")
    # cor = 0.458, sample = 55, p = 4.372361e-04
    
    # learning course 2: Propedeusethese
    plot(data$Propedeusethese, data$thesis_grades)
    abline(lm(data$thesis_grades ~ data$Propedeusethese), col="blue")
    # cor = 0.41985, sample = 132, p = 5.400573e-07
    
    # learning course 3: Wetens..en.Stat..Redeneren
    plot(data$Wetens..en.Stat..Redeneren, data$thesis_grades)
    abline(lm(data$thesis_grades ~ data$Wetens..en.Stat..Redeneren), col="blue")
    # cor = 0.30849, sample = 55, p = 2.193442e-02

#----------------------------------------------------------------
# track differences and thesis grades
    require(foreign)
    require(nnet)
    require(ggplot2)
    require(reshape2)
    data_grades1 = subset(data_grades, data_grades$Description == "M Psychologie")
    track_df = subset(data_grades1, select = c("Specialisation", "thesis_grades")) 
    # change track names so they belong to same group:
    #track_df1= data.frame(lapply(track_df, function(x){
    #                gsub("Track Training & Development", "Track Training and Development", x)
    #                gsub("Training & Development", "Track Training and Development", x)
    #                gsub("Inactief T&D", "Track Training and Development", x)
    #                gsub("Work & Organisational Psych", "Spec Work & Organ. Psychology", x)
    #                gsub("Spec W&O, route WHP", "Spec Work & Organ. Psychology", x)
    #                gsub("Spec B&C, route Cogn Neurosc", "Spec Brain & Cognition", x)
    #                gsub("Psycho. Gedragsbeïnvloeding", "Spec Social Psychology", x)
    #             }))
    table(track_df1)
    
    # plot mean thesis grades for each specialisation:
    plot(track_df$Specialisation, track_df$thesis_grades, las =2, par(mar = c(15, 6, 4, 2)+ 0.1),
    ylab = 'Thesis grades', xlab = 'Specialisation',cex.lab=1,
    par(cex.axis = 0.5),
    names = c("","General Psychology", "Inactief T&D", "Spec Brain & Cognition",
            "Spec Clinical Developmental Psych","Spec Clinical Neuropsychology",
            "Clinical Psychology","Developmental Psychology","Psychological Methods",
            "Social Psychology","Work & Organ. Psychology","Behaviour & Health",
            "Clinical Forensic Psych", "Sport & Performance Psych", "Training and Development"))
    
#-----------------------------------------------------------
# mean thesis grade for each course
    mean_grade = rep(NA, (length(data1[1,])-2))
    for(i in 1:a){
        mean_grade[i] = colMeans(data1[i+1], na.rm=TRUE)
    }
    mean_grade
    mean_matrix = data.frame(names(data1[,2:(a+1)]))
    mean_matrix$mean = mean_grade
    mean_matrix[order(mean_matrix$mean, decreasing=TRUE),]
    
    colMeans(mydata[sapply(mydata,is.numeric)])
    
    