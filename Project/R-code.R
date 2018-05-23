# Load data into R - wide data sorted by StudentID
full_data = read.csv("/Users/natalieglomsda/PycharmProjects/Methodology-Consulting/Project/full_data.csv")
full_data$Graduation.date <- format(as.Date(full_data$Graduation.date, format = "%d/%m/%Y"), "%d/%m/%Y")
subset(full_data, full_data$Graduation.date)

### Part 1. DATA PREPARATION

# pre 2014




# post 2014



#------------------------------------------------------
### Part 2. DATA MODELLING/ANALYSIS

### LOGISTIC REGRESSION
# need dataset with (1) thesis grade and (2) department - coded 1-7

### CORRELATION
# need dataset with (1) thesis grade and (2) duration of masters

### 


