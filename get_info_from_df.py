import pandas as pd

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

class DataFrameInfo:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def describe_columns(self):
        return self.dataframe.dtypes

    def extract_statistics(self):
        return self.dataframe.describe()

    def count_distinct_values(self):
        return self.dataframe.nunique()

    def print_shape(self):
        return self.dataframe.shape

    def count_null_values(self):
        return self.dataframe.isnull().sum()

    def percentage_null_values(self):
        total_rows = len(self.dataframe)
        return (self.dataframe.isnull().sum() / total_rows) * 100

df_info = DataFrameInfo(df)

#print(df_info.describe_columns()) # Describe all columns
#print(df_info.extract_statistics()) # Extract statistical values
#print(df_info.count_distinct_values()) # Count distinct values in categorical columns
#print(df_info.print_shape()) # Print out the shape of the df
#print(df_info.count_null_values()) # Generate a count of NULL values in each column
#print(df_info.percentage_null_values()) # Generate a percentage count of NULL values in each column