# This script demonstrates how to use R for data analysis tasks that have been
# previously performed in Excel. 
# 
# NOTE: This version contains 5 intentional typos/syntax errors for debugging practice.
# Find and fix them to make the script run!

# Loading the necessary libraries
library(tidyverse)
library(readxl)

# Assigning the path to a variable
path_to_file <- "data/ParkRunPerformanceData.xlsx"

# Reading data from an Excel file
data <- read_excel(path = path_to_file,
                   sheet = "Sheet1",
                   col_types = c("date", "numeric"))

# Exploring the data
head(data)

# Checking its structure
str(data)

# Calculating some summary statistics
summary(data)

# Rename the columns to ensure consistency and ease manipulation
names(data) <- c("date","runtime")

# Sorting the data
data_sorted <- data |> arrange(runtime)
data_sorted

data_sorted_inv <- data |> arrage(-runtime)  # ERROR 1
data_sorted_inv

# Calculating the summaries manually 
summary_dates <- 
  data |>
  summarise(min_date = min(date),
            max_date = max(date))
summary_dates

summary_runtimes <- 
  data |>
  summarise(
            count = n(),
            mean_runtime = mean(runtime),
            slowest = max(runtime),
            fastest = minn(runtime))  # ERROR 2
summary_runtimes

# Rounding the run times to the nearest minute
data_rounded <- data |> 
  mutate(runtime_mins = round(x = runtime, digits = 0))
data_rounded

# Counting the frequencies for each value
freq <- data_rounded |> 
  count(runtime_mins)

freq

# A quick histogram
hist(data_rounded$runtime_mins, breaks = 14:33)
# With the original data
hist(data$runtime, breaks = 14:33)

# A nicer histogram
data |> 
  ggplot(aes(x = runtime))+
  geom_histogram(binwidth = 1, col = "white", fill = "steelblue", alpha = 0.7)+
  labs(x = "Run time in seconds",
       y = "frequency",
       title = "Park Run Times Distribution",
       subtitle = "Records from Aug 2012 to Aug 2015",
       caption = "Source: Andrew Tomlinson")+
  scale_x_continuous(breaks = 14:33)+
  geom_hline(yintercept = 0, linewidth = 1, col = "grey30")+
  theme_minimal()+
  theme(title = element_text(size = '15'))  # ERROR 3

# Have the run times improved over the time period?
# Visualisation to explore temporal trends
data |> 
  ggplot(aes(x = date, y = runtime))+
  geom_point() +  
  geom_smooth(method = 'lm")  # ERROR 4

# Additional analysis: Finding the fastest and slowest runs
fastest_run <- data |>
  filter(runtime == min(runtime)) |>
  pull(date)

slowest_run <- data |>
  filter(runtime == max(runtime)) |>
  pull(date)

# ERROR 5
fastest_and_slowest <- data |>>
  slice_min(runtime) |>
  select(date, runtime)
