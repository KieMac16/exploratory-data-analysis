import pandas as pd

data = pd.read_csv("C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv")

# Use the dtypes attribute to check the data types of each column
data_types = data.dtypes

print(data_types)
