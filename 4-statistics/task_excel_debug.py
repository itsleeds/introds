# This script demonstrates how to use Python for data analysis tasks that have been
# previously performed in Excel, replicating the logic from task_excel.R

# NOTE: This version contains intentional typos/syntax errors for debugging practice.
# Find and fix them to make the script run!

import polars as pl
import pandas as pd # Used for reading Excel files
import seaborn as sns
import matplotlib.pyplot as plt

# Set the style for plots
sns.set_theme(style="whitegrid") # equivalent to theme_minimal() mostly

# Assigning the path to a variable
# Note: Path relative to the project root
path_to_file = "00_data/ParkRunPerformanceData.xlsx"

# Reading data from an Excel file
# Using pandas to read excel as it relies on openpyxl which is installed
data = pl.from_pandas(pd.read_excel(path_to_file, sheet_name="Sheet1"))

# Exploring the data
print("---"Head of Data"---")
print(data.head())

# Checking its structure (schema in Polars)
print("\n--- Schema ---")
print(data.schema)

# Calculating some summary statistics
print("\n--- Summary Statistics ---")
print(data.describe())

# Rename the columns to ensure consistency and ease manipulation
# R: names(data) <- c("date","runtime")
# We assume the first two columns are what we want, based on R script context
if len(data.columns) >= 2:
    data = data.rename({data.columns[0]: "date", data.columns[1]: "run_time"}) # ERROR 1: Wrong column name
    # Ensure runtime is numeric and date is date (if not already)
    # R's read_excel with col_types = c("date", "numeric") handles this.
    # Pandas usually infers well.
else:
    print("Warning: Data does not have at least 2 columns to rename.")

# Sorting the data
data_sorted = data.sort_by("run_time") # ERROR 2: Wrong method name, should be .sort()
print("\n--- Sorted Data (Ascending) ---")
print(data_sorted)

data_sorted_inv = data.sort("run_time", descending=True) # Will fail if run_time is not found
print("\n--- Sorted Data (Descending) ---")
print(data_sorted_inv)


# Calculating the summaries manually 
summary_dates = data.select([
    pl.col("date").min().alias("min_date"),
    pl.col("date").max().alias("max_date")
])
print("\n--- Summary Dates ---")
print(summary_dates)

summary_runtimes = data.select([
    pl.len(), # ERROR 3: Missing alias for summary
    pl.col("run_time").mean().alias("mean_runtime"),
    pl.col("run_time").max().alias("slowest"),
    pl.col("run_time").min().alias("fastest")
])
print("\n--- Summary Runtimes ---")
print(summary_runtimes)

# Rounding the run times to the nearest minute
data_rounded = data.with_columns(
    pl.col("run_time").round(0).alias("runtime_mins")
)
print("\n--- Data with Rounded Runtimes ---")
print(data_rounded.head())


# Counting the frequencies for each value
freq = data_rounded.group_by("runtime_mins").len().sort("runtime_mins")
print("\n--- Frequencies ---")
print(freq)

# A quick histogram
plt.figure()
plt.histogram(data_rounded["runtime_mins"], bins=range(14, 34)) # ERROR 4: Matplotlib hist typo
plt.title("Quick Histogram")
# plt.show() # Commented out to allow batch execution without blocking

# A nicer histogram using Seaborn (closer to ggplot)
plt.figure(figsize=(10, 6))
sns.histplot(
    data=data_rounded.to_pandas(), 
    binwidth=1, # ERROR 5: Missing 'x' argument
    color="steelblue", 
    edgecolor="white", 
    alpha=0.7
)
plt.title("Park Run Times Distribution\nRecords from Aug 2012 to Aug 2015", fontsize=15)
plt.xlabel("Run time in seconds")
plt.ylabel("frequency")
plt.xlim(14, 33)
plt.axhline(0, color="grey", linewidth=1)

# Add caption equivalent
plt.figtext(0.8, 0.01, "Source: Andrew Tomlinson", wrap=True, horizontalalignment='center', fontsize=10)

# plt.show() # Commented out

# Have the run times improved?
# A different exploration
plt.figure(figsize=(10, 6))
# Regplot fits a linear regression model
sns.regplot(
    data=data.to_pandas(), 
    x=pd.to_numeric(data["date"].to_pandas()), # Regression needs numeric x
    y="run_time", # Will fail due to "run_time" column if previous code is not fixed
    scatter_kws={'s':10}, 
    line_kws={'color':'blue'}
)
# Fix x-axis labels to show dates instead of numbers
# This is a bit involved in matplotlib/seaborn compared to ggplot
import matplotlib.dates as mdates
ax = plt.gca()
# We need to map the numeric dates back to proper date locators if we want them pretty
# But strictly replicating the 'quick' nature:
plt.title("Run Times over Date")
# plt.show() # Commented out
