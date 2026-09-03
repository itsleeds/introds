# This script demonstrates how to use Python (pandas) for data analysis tasks that have been
# previously performed in Excel, replicating the logic from Task_excel.R.
# Note: For large datasets, high-performance alternatives include Polars (https://docs.pola.rs/)
# and DuckDB (https://duckdb.org/).

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set the style for plots
sns.set_theme(style="whitegrid")

# Path to data
path_to_file = "00_data/ParkRunPerformanceData.xlsx"

# Reading data from an Excel file
data = pd.read_excel(path_to_file, sheet_name="Sheet1")

# Exploring the data
print("--- Head of Data ---")
print(data.head())

# Checking its structure and data types
print("\n--- Info ---")
data.info()

# Calculating summary statistics
print("\n--- Summary Statistics ---")
print(data.describe())

# Rename columns
if len(data.columns) >= 2:
    data.columns = ["date", "runtime"]
else:
    print("Warning: Data does not have at least 2 columns to rename.")

# Sorting the data
data_sorted = data.sort_values(by="runtime")
print("\n--- Sorted Data (Ascending) ---")
print(data_sorted.head())

data_sorted_inv = data.sort_values(by="runtime", ascending=False)
print("\n--- Sorted Data (Descending) ---")
print(data_sorted_inv.head())

# Calculating summaries manually
print("\n--- Summary Dates ---")
print(f"min_date: {data['date'].min()}, max_date: {data['date'].max()}")

print("\n--- Summary Runtimes ---")
summary_runtimes = pd.Series({
    "count": data["runtime"].count(),
    "mean_runtime": data["runtime"].mean(),
    "slowest": data["runtime"].max(),
    "fastest": data["runtime"].min()
})
print(summary_runtimes)

# Rounding run times to the nearest minute
data["runtime_mins"] = data["runtime"].round(0)
print("\n--- Data with Rounded Runtimes ---")
print(data.head())

# Counting frequencies for each value
freq = data["runtime_mins"].value_counts().sort_index()
print("\n--- Frequencies ---")
print(freq)

# Quick histogram
plt.figure()
plt.hist(data["runtime_mins"], bins=range(14, 34))
plt.title("Quick Histogram")

# Nicer histogram using Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(
    data=data, 
    x="runtime", 
    binwidth=1, 
    color="steelblue", 
    edgecolor="white", 
    alpha=0.7
)
plt.title("Park Run Times Distribution\nRecords from Aug 2012 to Aug 2015", fontsize=15)
plt.xlabel("Run time in seconds")
plt.ylabel("frequency")
plt.xlim(14, 33)
plt.axhline(0, color="grey", linewidth=1)
plt.figtext(0.8, 0.01, "Source: Andrew Tomlinson", wrap=True, horizontalalignment='center', fontsize=10)

# Have the run times improved?
plt.figure(figsize=(10, 6))
data_reg = data.copy()
data_reg["date_num"] = mdates.date2num(data_reg["date"])
sns.regplot(
    data=data_reg,
    x="date_num",
    y="runtime",
    scatter_kws={'s': 10},
    line_kws={'color': 'blue'}
)
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.title("Run Times over Date")
