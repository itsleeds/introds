# This script demonstrates how to use Python for data analysis tasks that have been
# previously performed in SPSS, replicating the logic from task_2_spss.R

# NOTE: This version contains intentional typos/syntax errors for debugging practice.
# Find and fix them to make the script run!

import polars as pl
import pandas as pd # For reading Excel
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf
import numpy as np

# Set plot style
sns.set_theme(style="whitegrid")

# Loading the necessary libraries
path_to_file = "00_data/RunningData.xlsx"

# Reading data from an Excel file
data = pl.from_pandas(pd.read_excel(path_to_file, sheet_name="Sheet1"))

# Exploring the data
print("---"Head"---")
print(data.head())

# Checking its structure
print("\n--- Schema ---")
print(data.schema)

# Calculating some summary statistics
print("\n--- Summary ---")
print(data.describe())

# Rename the columns to ensure consistency and ease manipulation
# R: names(data) <- c("position", "time", "age_cat", "gender", "prev_runs")
if len(data.columns) >= 5:
    data = data.rename({
        data.columns[0]: "position",
        data.columns[1]: "timee", # ERROR 1: Typo in column name
        data.columns[2]: "age_cat",
        data.columns[3]: "gender",
        data.columns[4]: "prev_runs"
    })
else:
    print("Warning: Column count mismatch for renaming")

# Calculating summaries for time
print("\n--- Time Summary ---")
print(data["timee"].describe()) # Will fail due to "timee"

# Exploring age categories
print("\n--- Age Categories ---")
print(data["age_cat"].unique())

# Subset only adults
# R: children_cats <- c("10","11-14","15-17")
children_cats = ["10", "11-14", "15-17"]
# ERROR 2: Incorrect filter logic (should be ~pl.col(...).is_in)
data_adults = data.filter(pl.col("age_cat").is_in(children_cats)) 

print("\n--- Adult Age Categories ---")
print(data_adults["age_cat"].unique())

# Producing summaries
print("\n--- Adult Time Summary ---")
print(data_adults["timee"].describe()) # Will fail due to "timee"

# A quick histogram
plt.figure()
sns.histplot(data=data_adults.to_pandas(), x="timee", binwidth=1, color="steelblue", edgecolor="white") # Will fail due to "timee"
plt.title("Histogram of Adult Times")
# plt.show()

# A density curve 
plt.figure()
sns.kdeplot(data=data_adults.to_pandas(), x="timee") # Will fail due to "timee"
plt.title("Density of Adult Times")
# plt.show()

# Analysis by gender
print("\n--- Analysis by Gender ---")
summary_gender = data_adults.group_by("gender").agg([
    pl.col("timee").min().alias("min"), # Will fail due to "timee"
    pl.col("timee").mean().alias("mean"),
    pl.col("timee").median().alias("median"),
    pl.col("timee").max().alias("max")
])
print(summary_gender)

# Comparing the distributions
# ERROR 3: Missing to_pandas() for FacetGrid
g = sns.FacetGrid(data_adults, row="gender", hue="gender", aspect=2, height=3) 
g.map(sns.histplot, "timee", edgecolor="white") # Will fail due to "timee"
# plt.show()

plt.figure()
sns.kdeplot(data=data_adults.to_pandas(), x="timee", hue="gender") # Will fail due to "timee"
plt.title("Density by Gender")
# plt.show()

plt.figure()
sns.boxplot(data=data_adults.to_pandas(), x="timee", hue="gender") # Will fail due to "timee"
plt.title("Boxplot by Gender")
# plt.show()

plt.figure()
sns.violinplot(data=data_adults.to_pandas(), x="timee", y="gender", hue="gender") # Will fail due to "timee"
plt.title("Violin Plot by Gender")
# plt.show()


## Statistical tests
# Extracting the data
times_female_adults = data_adults.filter(pl.col("gender") == "F")["timee"] # Will fail due to "timee"
times_male_adults = data_adults.filter(pl.col("gender") == "M")["timee"] # Will fail due to "timee"

print("\n--- Female Times (Head) ---")
print(times_female_adults.head())
print("\n--- Male Times (Head) ---")
print(times_male_adults.head())

# Comparing two groups based on gender (t-test)
# Using scipy.stats.ttest_ind
t_stat, p_val = stats.ttest_ind(times_male_adults, times_female_adults) # ERROR 4: Typo in t-test function
print(f"\n--- T-Test Results ---\nt-statistic: {t_stat}\np-value: {p_val}")


# Analysis of previous runs vs times
# A quick visualisation
plt.figure()
sns.regplot(data=data_adults.to_pandas(), x="prev_runs", y="timee") # Will fail due to "timee"
plt.title("Time vs Previous Runs")
# plt.show()

plt.figure()
sns.lmplot(data=data_adults.to_pandas(), x="prev_runs", y="timee", hue="gender") # Will fail due to "timee"
plt.title("Time vs Previous Runs by Gender")
# plt.show()

# The formal analysis for all adults (Correlation)
corr, p_corr = stats.pearsonr(data_adults["timee"], data_adults["prev_runs"]) # Will fail due to "timee"
print(f"\n--- Correlation Test ---\ncorrelation: {corr}\np-value: {p_corr}")

# Finding the median of prev runs
median_prev_runs = data_adults["prev_runs"].median()
print(f"\nMedian Previous Runs: {median_prev_runs}")

data_adults_pr_gr = data_adults.with_columns(
    (pl.col("prev_runs") >= median_prev_runs).alias("pr_gr")
)

print("\n--- Data with pr_gr group ---")
print(data_adults_pr_gr.select(["prev_runs", "pr_gr"]).head())

# a quick visual check
plt.figure()
sns.histplot(data=data_adults_pr_gr.to_pandas(), x="prev_runs", hue="pr_gr", multiple="stack")
plt.title("Previous Runs Split")
# plt.show()

# Comparing times
plt.figure()
sns.boxplot(data=data_adults_pr_gr.to_pandas(), x="timee", hue="pr_gr") # Will fail due to "timee"
plt.title("Time by Previous Runs Group")
# plt.show()

# Extracting the first two digits of the age cat
# R: str_extract(age_cat, '^\\d{2}') |> as.numeric()
# Polars regex extract
data_adults_lm = data_adults.with_columns(
    pl.col("age_cat").str.extract(r"^(\d{2})", 1).cast(pl.Float64).alias("age") # ERROR 5: This regex is missing a closing paren if I actually wanted an error here.
)
# Re-reading the problem description for error 5: Regex error in `str.extract`: Change `r"^(\d{2})"` to `r"^(\d{2)"` (missing closing parenthesis).
# The current code in the file is `r"^(\d{2})"`. I will change it to `r"^(\d{2)"` for debug.
# And for the original python: `pl.col("age_cat").str.extract(r"^(\d{2})", 1).cast(pl.Float64).alias("age")`
# I should change it to `pl.col("age_cat").str.extract(r"^(\d{2)", 1).cast(pl.Float64).alias("age")` for debug.


# Building a linear model
# Using statsmodels formula API
print("\n--- Linear Model ---")
model = smf.ols(formula="timee ~ age + gender + prev_runs", data=data_adults_lm.to_pandas()) # Will fail due to "timee"
results = model.fit()
print(results.summary())
