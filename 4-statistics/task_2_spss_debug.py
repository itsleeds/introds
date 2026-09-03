# This script demonstrates how to use Python (pandas) for data analysis tasks that have been
# previously performed in SPSS, replicating the logic from Task_2_SPSS.R.
#
# NOTE: This version contains intentional typos/syntax errors for debugging practice.
# Find and fix them to make the script run!

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf

# Set plot style
sns.set_theme(style="whitegrid")

# Path to data
path_to_file = "00_data/RunningData.xlsx"

# Reading data from an Excel file
data = pd.read_excel(path_to_file, sheet_name="Sheet1")

# Exploring the data
print("--- Head ---")
print(data.head())

# Checking its structure
print("\n--- Info ---")
data.info()

# Summary statistics
print("\n--- Summary ---")
print(data.describe())

# Rename columns
if len(data.columns) >= 5:
    data.columns = ["position", "time", "age_cat", "gender", "prev_runs"]
else:
    print("Warning: Column count mismatch for renaming")

# Summaries for time
print("\n--- Time Summary ---")
print(data["time"].describe())

# Exploring age categories
print("\n--- Age Categories ---")
print(data["age_cat"].unique())

# Subset only adults
children_cats = ["10", "11-14", "15-17"]
data_adults = data[~data["age_cat"].isin(children_cats) # ERROR 1: Missing closing square bracket

print("\n--- Adult Age Categories ---")
print(data_adults["age_cat"].unique())

# Producing summaries
print("\n--- Adult Time Summary ---")
print(data_adults["time"].describe())

# A quick histogram
plt.figure()
sns.histplot(data=data_adults, x="timee", binwidth=1, color="steelblue", edgecolor="white") # ERROR 2: Column name typo ('timee')
plt.title("Histogram of Adult Times")

# A density curve 
plt.figure()
sns.kdeplot(data=data_adults, x="time")
plt.title("Density of Adult Times")

# Analysis by gender
print("\n--- Analysis by Gender ---")
summary_gender = data_adults.groupby("gender")["time"].agg(["min", "mean", "median", "max"])
print(summary_gender)

# Comparing distributions
g = sns.FacetGrid(data_adults, row="gender", hue="gender", aspect=2, height=3)
g.map(sns.histplot, "time", edgecolor="white")

plt.figure()
sns.kdeplot(data=data_adults, x="time", hue="gender")
plt.title("Density by Gender")

plt.figure()
sns.boxplot(data=data_adults, x="time", hue="gender")
plt.title("Boxplot by Gender")

plt.figure()
sns.violinplot(data=data_adults, x="time", y="gender", hue="gender")
plt.title("Violin Plot by Gender")

## Statistical tests
# Extracting data
times_female_adults = data_adults[data_adults["gender"] == "F"]["time"]
times_male_adults = data_adults[data_adults["gender"] == "M"]["time"]

print("\n--- Female Times (Head) ---")
print(times_female_adults.head())
print("\n--- Male Times (Head) ---")
print(times_male_adults.head())

# Comparing two groups based on gender (t-test)
t_stat, p_val = stats.ttest_ind(times_male_adults) # ERROR 3: Missing second sample argument (times_female_adults)
print(f"\n--- T-Test Results ---\nt-statistic: {t_stat}\np-value: {p_val}")

# Analysis of previous runs vs times
plt.figure()
sns.regplot(data=data_adults, x="prev_runs", y="time")
plt.title("Time vs Previous Runs")

plt.figure()
sns.lmplot(data=data_adults, x="prev_runs", y="time", hue="gender")
plt.title("Time vs Previous Runs by Gender")

# Formal correlation test
corr, p_corr = stats.pearsonr(data_adults["time"], data_adults["prev_runs"])
print(f"\n--- Correlation Test ---\ncorrelation: {corr}\np-value: {p_corr}")

# Finding median of prev runs
median_prev_runs = data_adults["prev_runs"].median()
print(f"\nMedian Previous Runs: {median_prev_runs}")

data_adults["pr_gr"] = data_adults["prev_runs"] >= median_prev_runs

print("\n--- Data with pr_gr group ---")
print(data_adults[["prev_runs", "pr_gr"]].head())

# Visual check
plt.figure()
sns.histplot(data=data_adults, x="prev_runs", hue="pr_gr", multiple="stack")
plt.title("Previous Runs Split")

# Comparing times
plt.figure()
sns.boxplot(data=data_adults, x="time", hue="pr_gr")
plt.title("Time by Previous Runs Group")

# Extract first two digits of age category for numeric proxy
data_adults["age"] = data_adults["age_cat"].str.extract(r"^(\d{2})").astype(float)

# Building a linear model
print("\n--- Linear Model ---")
model = smf.ols(formula="time ~ age + gender + prev_runs", data=data_adults)
results = model # ERROR 4: Forgot to call .fit() on the model object
print(results.summary())
