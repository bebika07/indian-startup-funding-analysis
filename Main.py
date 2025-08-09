import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# 1. Load Data
# ---------------------------
# Replace with your dataset path
try:
    df = pd.read_csv("startup_funding.csv")
    print("Data loaded successfully.")
except FileNotFoundError:
    print("Error: 'startup_funding.csv' not found. Please upload the file or check the path.")
    exit()


print("Initial Data Preview:")
print(df.head())

# ---------------------------
# 2. Standardize Column Names
# ---------------------------
# Standardize column names by converting to lowercase and replacing spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Print standardized column names to verify
print("\nStandardized Column Names:")
print(df.columns)


# ---------------------------
# 3. Date Cleaning
# ---------------------------
# Convert the date column to datetime objects, coercing errors
df['date_dd/mm/yyyy'] = pd.to_datetime(df['date_dd/mm/yyyy'], errors='coerce')

# Drop rows where the date is invalid
df = df.dropna(subset=['date_dd/mm/yyyy'])

print("\nData after Date Cleaning:")
print(df.head())

# ---------------------------
# 4. Handle Null Values
# ---------------------------
# Fill missing values and standardize string columns
df['startup_name'] = df['startup_name'].fillna("Unknown").str.strip().str.title()
df['industry_vertical'] = df['industry_vertical'].fillna("Unknown").str.strip().str.title()
df['amount_in_usd'] = df['amount_in_usd'].fillna("0") # Fill AmountInUsd before cleaning format

print("\nData after Handling Null Values:")
print(df.head())

# ---------------------------
# 5. Clean Funding Amount Format
# ---------------------------
# Remove non-digit characters except '.' and convert to numeric
df['amount_in_usd'] = df['amount_in_usd'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['amount_in_usd'] = pd.to_numeric(df['amount_in_usd'], errors='coerce').fillna(0)

print("\nData after Cleaning Amount Format:")
print(df.head())


# ---------------------------
# 6. Remove Duplicates
# ---------------------------
# Remove duplicate rows based on key columns
initial_rows = len(df)
df.drop_duplicates(subset=['startup_name', 'date_dd/mm/yyyy', 'investors_name', 'amount_in_usd'], inplace=True)
rows_after_dropping_duplicates = len(df)
print(f"\nRemoved {initial_rows - rows_after_dropping_duplicates} duplicate rows.")
print("Data after Removing Duplicates:")
print(df.head())

# ---------------------------
# 7. Analysis
# ---------------------------
total_funding = df['amount_in_usd'].sum()
avg_funding = df['amount_in_usd'].mean()

top_startups = df.groupby('startup_name')['amount_in_usd'].sum().sort_values(ascending=False).head(10)
top_industries = df.groupby('industry_vertical')['amount_in_usd'].sum().sort_values(ascending=False).head(10)
funding_trend = df.groupby(df['date_dd/mm/yyyy'].dt.to_period('M'))['amount_in_usd'].sum()

print(f"\nTotal Funding: ${total_funding:,.0f}")
print(f"Average Funding per Deal: ${avg_funding:,.0f}")
print("\nTop 10 Startups by Funding:")
print(top_startups)
print("\nTop 10 Industries by Funding:")
print(top_industries)

# ---------------------------
# 8. Visualizations
# ---------------------------
plt.figure(figsize=(12, 6))
funding_trend.plot(kind='line', marker='o', title='Funding Trend Over Time')
plt.ylabel("Funding Amount ($)")
plt.xlabel("Month")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
top_startups.plot(kind='bar', title='Top 10 Startups by Funding')
plt.ylabel("Total Funding ($)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
top_industries.plot(kind='bar', title='Top 10 Industries by Funding')
plt.ylabel("Total Funding ($)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()