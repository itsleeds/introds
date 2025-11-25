# This script demonstrates how to use R for data analysis tasks that have been
# previously performed in SPSS. 


# Loading the necessary libraries
library(tidyverse)
library(readxl)

# Assigning the path to a variable
path_to_file <- "00_data/RunningData.xlsx"

# Reading data from an Excel file
data <- read_excel(path = path_to_file,
  sheet = "Sheet1")


# Exploring the data
head(data)

# Checking its structure
str(data)

# Calculating some summary statistics
summary(data)


# Rename the columns to ensure consistency and ease manipulation
names(data) <- c("position", "time", "age_cat", "gender", "prev_runs")


# calculating summaries

summary(data$time)


# Exploring age categories

data$age_cat |> unique() 


# Subset only adults 

children_cats <- c("10","11-14","15-17")

data_adults <- data |> 
  filter(!age_cat %in% children_cats)

data_adults$age_cat |> unique() 

# Producing summaries
summary(data_adults$time)

# A quick histogram
data_adults |> 
  ggplot(aes(x = time))+
  geom_histogram(binwidth = 1, col = "white", fill = "steelblue")  

# A density curve 
data_adults |> 
  ggplot(aes(x = time))+
  geom_density()

# Analysis by gender

data_adults |> 
  group_by(gender) |> 
  summarise(min = min(time),
  mean = mean(time),
  median = mean(time),
  max = max(time))

# Comparing the distributions

data_adults |> 
  ggplot(aes(x = time, fill = gender))+
  geom_histogram(col = "white")+
  facet_grid(gender~.)


data_adults |> 
  ggplot(aes(x = time, col = gender))+
  geom_density()

data_adults |> 
  ggplot(aes(x = time, col = gender))+
  geom_boxplot()

data_adults |> 
  ggplot(aes(x = time, y = gender, col = gender))+
  geom_violin()


## Statistical tests
# Extracting the data

times_female_adults <- data_adults |> 
  filter(gender == "F") |> 
  pull(time)

times_female_adults

times_male_adults <- data_adults |> 
  filter(gender == "M") |> 
  pull(time)

times_male_adults

# Comparing two groups based on gender
t.test(times_male_adults,times_female_adults)


# Analysis of previous runs vs times
# A quick visualisation

data_adults |> 
  ggplot(aes(x = prev_runs, y =time))+
  geom_point()+
  geom_smooth(method = "lm")

data_adults |> 
  ggplot(aes(x = prev_runs, y =time, col = gender))+
  geom_point() +
  geom_smooth(method = "lm")

# The formal analysis for all adults
cor.test(data_adults$time,data_adults$prev_runs)

# Finding the median of prev runs
median_prev_runs <- median(data_adults$prev_runs)
median_prev_runs

data_adults_pr_gr <- data_adults |> 
  mutate(pr_gr = prev_runs>=median_prev_runs)

data_adults_pr_gr

# Another way to do it
data_adults |> 
  mutate(pr_gr = prev_runs>=median(prev_runs))

# a quick visual check
data_adults_pr_gr |> 
  ggplot(aes(prev_runs,fill = pr_gr))+
  geom_histogram()

# Comparing times
data_adults_pr_gr |> 
  ggplot(aes(x = time, col = pr_gr))+
  geom_boxplot()

# Extracting the first two digits of the age cat
data_adults_lm <- data_adults |> 
  mutate(age = str_extract(age_cat, '^\\d{2}') |> as.numeric())  

# Building a linear model
my_linear_model <- lm(formula = "time ~ age + gender + prev_runs", data = data_adults_lm) 

summary(my_linear_model)

