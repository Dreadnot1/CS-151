import pandas as pd
import os
from pathlib import Path

load_path = r'C:test'

df = pd.read_csv(load_path) #where df stands for dataframe

print(df.head()) #gives you the first five lines of the file

print(df.info()) #tells you about count, missing, data types

print(df.describe())

print(df["Age"].mean())

#Filtering
under_thirty = df[df["Age"] > 30] #creates a new dataframe where age is greater than 30
print(under_thirty.head())
print(under_thirty.info())

london = df[df["City"] == "London"]
print(london.head())
print(london.describe())

#Add a column
df["YearsUntilRetirement"] = 65 - df["Age"]
print(df[["Name", "Age", "YearsUntilRetirement"]])

#Looking for Alice. She might be in Wonderland...
alice = df[df["Name"] == "Alice"]
print(alice)

#Grouping data
print(df.groupby("Occupation")["Salary"].mean())
print(df.groupby("City")["Age"].mean())

#Sorting data
print(df.sort_values(by="Salary",ascending=False)[["Name","Occupation","Salary"]])

#Saving the data
output_file = 'retirement.csv'
output_dir = Path('C:/Users/Devin/Documents/Test Files')
output_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(output_dir, index=False)  # can join path elements with / operator