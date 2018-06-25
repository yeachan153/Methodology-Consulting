#install.packages("readxl")
library(dplyr)
library(readxl)
install.packages(c("tidyr","devtools"))
library(tidyr)
library(devtools)
library(dplyr)
library(lattice)
install.packages("ggplot")
library(ggplot)
#------------------------------------------------------
# Part 1. THESIS GRADES
# PRE 2014
data_grades = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/PRE2014.csv")

# 1. extract columns with "Thesis" (coded for Research Masters students) & "these" (other tracks):
    thesis_cols = data_grades[,grepl("Thesis", names(data_grades))]
    these_cols = data_grades[,grepl("these",  names(data_grades))]
    scriptie_cols = data_grades[,grepl("Scriptie", names(data_grades))]
    werkstuk_cols = data_grades[,grepl("Werkstuk", names(data_grades))]

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
    range(thesis_grade_df$thesis_grades)

    # Issues:
    range(thesis_grades) 
    thesis_grade_df[thesis_grade_df$thesis_grades > 10,] 
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades > 10,]) #10
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades == 0,]) # 62
    nrow(thesis_grade_df[thesis_grade_df$thesis_grades == 10,]) # 3
    
    
# create csv file for studentID and thesis grade table 
    setwd("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project") 
    #write.csv(thesis_grade_df, file = "Thesis_Grades.csv",row.names = FALSE)


# Adding thesis grade to Master Dataframe.xlsx file:
    #master_df = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/Master Dataframe.csv")
    #merged_df = merge(x = master_df, y = thesis_grade_df, by = 'StudentID', all.x = TRUE)
    #write.csv(thesis_grade_df, file = "merged_thesis.csv")

#-------------------------------------------------------------
# Part 2. CORRELATIONS FOR EACH COURSE AGAINST THESIS GRADES

    # for pre 2014
    data = data_grades%>%select(-thesis_grades,thesis_grades) #thesis_grade at the end of the df
    data = data[,c(2, 13:length(data))]
    head(data)
    
    # some columns only have NAs or < 3 values; we should exclude these columsn because cor.test() doesn't work for these columns
    nrow(data)
    data1 = data[,colSums(is.na(data)) < 634] # since we have 637 nrows - at least 3 of it should not be NA
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
    cor_matrix2 = subset(cor_matrix1, cor_matrix1$cor >= .4)
    names(cor_matrix2) = c("course_name","cor","sample","p.value") # rename colnames
    cor_matrix3 = cor_matrix2[!grepl("Thesis", cor_matrix2$course_name),] #exclude thesis columns
    cor_matrix4 = cor_matrix3[!grepl("these", cor_matrix3$course_name),]  #exclude these columns
    
    cor_table_output = cor_matrix4[order(cor_matrix4$cor, decreasing=TRUE),]
    write.csv(cor_table_output, file = "Correlation_Msc_PRE2014.csv",row.names = FALSE)
    nrow(cor_matrix4) # 15 courses with correlation > 0.5 & sample > 15  (all sig p.values)


#################-----------------------------------------------------------
    ### POST DATA
    data_post = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/POST2014.csv")
    nrow(data_post) #254 people after 2014
    
    data2 = data_post%>%select(-thesis_grades,thesis_grades) #thesis_grade at the end of the df
    data2 = data2[,c( 2, 13:length(data2))]
    head(data2)
    
    # some columns only have NAs or < 3 values; we should exclude these columsn because cor.test() doesn't work for these columns
    nrow(data2)
    data2 = data2[,colSums(is.na(data2)) < 251] # since we have 254 nrows - at least 3 of it should not be NA
    ncol(data2) # data1 excludes 56 courses
    
    a = length(data2[1,])-2
    correlations = rep(NA, (length(data2[1,])-2))
    size = rep(NA, (length(data2[1,])-2) )
    p_value = rep(NA, (length(data2[1,])-2) )
    
    # correlations:
    for (i in 1:a){
        correlations[i] = cor(data2[,i+1],data2$thesis_grades, use = "pairwise.complete.obs", method="spearman")
    }
    #sample size:
    for(i in 1:a){
        size[i]= cor.test((data2[,i + 1]), data2$thesis_grades)$parameter + 2
    }
    #p-value
    for (i in 1:a){
        p_value[i] = cor.test(data2[, i+1], data2$thesis_grades)$p.value
    }
    
    cor_matrix2 = data.frame(names(data2[,2:(a+1)]))
    cor_matrix2$cor = correlations
    cor_matrix2$sample = size
    cor_matrix2$p.value = p_value
    cor_matrix2
    
    # use cor_matrix with sample > 15 
    cor_matrix_post1 = subset(cor_matrix2, cor_matrix2$sample > 15)
    # correlation higher than .5:
    cor_matrix_post2 = subset(cor_matrix_post1, cor_matrix_post1$cor >= .4)
    names(cor_matrix_post2) = c("course_name","cor","sample","p.value") # rename colnames
    cor_matrix_post3 = cor_matrix_post2[!grepl("Thesis", cor_matrix_post2$course_name),] #exclude thesis columns
    cor_matrix_post4 = cor_matrix_post3[!grepl("these", cor_matrix_post3$course_name),]  #exclude these columns
    
    cor_table_output2 = cor_matrix_post4[order(cor_matrix_post4$cor, decreasing=TRUE),]
    write.csv(cor_table_output2, file = "Correlation_Msc_POST2014.csv",row.names = FALSE)
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
    
    table(track_df)
    # plot mean thesis grades for each specialisation:
    par(mar=c(8,4,4,4))
    plot(track_df$Specialisation, track_df$thesis_grades, las=2,
         col=terrain.colors(4),ylab = 'Thesis grades',cex.lab=.8, par(cex.axis=0.7))
    
    # Descriptives of specialisations:
    levels(track_df$Specialisation)
    library(dplyr)
    descriptives_track = group_by(track_df, Specialisation) %>%
                    summarise(
                    count = n(),
                    mean = mean(thesis_grades, na.rm = TRUE),
                    sd = sd(thesis_grades, na.rm = TRUE))
    # One-way ANOVA:
    res.aov <- aov(thesis_grades ~ Specialisation, data = track_df)
    # Summary of the analysis
    summary(res.aov) # sig p-value
    # Post-hoc
    posthoc=TukeyHSD(res.aov)

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


    