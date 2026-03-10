import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("people_data.csv")

df["Age"].plot(kind="hist",bins=4,color="skyblue",edgecolor="black",title="Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

avg_salary = df.groupby("Occupation")["Salary"].mean()
avg_salary.plot(kind="barh", color="green", title="Average Salary by Occupation")
plt.xlabel("Average Salary")
plt.ylabel("Occupation")
plt.show()