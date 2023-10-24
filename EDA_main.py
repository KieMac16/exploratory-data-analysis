import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import missingno as msno

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

class DataTransform:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_to_numeric(self, column_name):
        self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name], errors='coerce')

    def convert_to_date(self, column_name, date_format='%b-%Y'):
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format=date_format, errors='coerce')

    def make_categorical(self, column_name):
        self.dataframe[column_name] = self.dataframe[column_name].astype('category')

    def convert_to_boolean(self, column_name, true_values=['y'], false_values=['n']):
        self.dataframe[column_name] = self.dataframe[column_name].isin(true_values)

    def remove_excess_symbols(self, column_name, symbol_to_remove):
        self.dataframe[column_name] = self.dataframe[column_name].str.replace(symbol_to_remove, '')
        
column_transform = DataTransform(df)

# Remove excess symbols from column(s) - I've made this but don't think I need it upon inspecting the data
column_transform.remove_excess_symbols('employment_length','<')
column_transform.remove_excess_symbols('employment_length','+')
column_transform.remove_excess_symbols('employment_length','year')
column_transform.remove_excess_symbols('employment_length','years')
column_transform.remove_excess_symbols('term','months')

# Convert column(s) to numerical format
column_transform.convert_to_numeric('mths_since_last_delinq')
column_transform.convert_to_numeric('mths_since_last_record')
column_transform.convert_to_numeric('term')
column_transform.convert_to_numeric('employment_length')

# Convert column(s) to date format
column_transform.convert_to_date('issue_date', date_format='%b-%Y')
column_transform.convert_to_date('earliest_credit_line', date_format='%b-%Y')
column_transform.convert_to_date('last_payment_date', date_format='%b-%Y')
column_transform.convert_to_date('next_payment_date', date_format='%b-%Y')
column_transform.convert_to_date('last_credit_pull_date', date_format='%b-%Y')

# Convert column(s) to categorical
column_transform.make_categorical('grade')
column_transform.make_categorical('sub_grade')
column_transform.make_categorical('home_ownership')
column_transform.make_categorical('verification_status')
column_transform.make_categorical('loan_status')
column_transform.make_categorical('application_type')

# Convert column(s) to boolean:
column_transform.convert_to_boolean('payment_plan')

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

class DataFrameTransform:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def count_null_values(self):
        return self.dataframe.isnull().sum()
    
    def impute_missing(self, column_name, impute_with='mean'):
        if impute_with == 'mean':
            self.dataframe[column_name].fillna(self.dataframe[column_name].mean(), inplace=True)
        elif impute_with == 'median':
            self.dataframe[column_name].fillna(self.dataframe[column_name].median(), inplace=True)
        elif impute_with == 'mode':
            self.dataframe[column_name].fillna(self.dataframe[column_name].mode(), inplace=True)
        else:
            ValueError

transform_df = DataFrameTransform(df)

'''Based on analysis in df_transform.py I am ready to drop the following columns'''
columns_to_drop = ['mths_since_last_delinq',
                   'mths_since_last_record',
                   'next_payment_date',
                   'mths_since_last_major_derog',
                   ]
df.drop(columns_to_drop, axis=1, inplace=True)

'''Based on analysis in df_transform.py I will forward fill the following columns'''
df['last_payment_date'].fillna(method='ffill', inplace=True)
df['collections_12_mths_ex_med'].fillna(method='ffill', inplace=True) # I chose this over mean/median intentionally
df['last_credit_pull_date'].fillna(method='ffill', inplace=True)

'''I am going to impute the following with the mean or median'''
transform_df.impute_missing('funded_amount','median') # Need to investigate further with outliers
transform_df.impute_missing('int_rate','mean') # Very similar to the median
transform_df.impute_missing('term','mean') # Only between 2 values
transform_df.impute_missing('employment_length','median')

print(transform_df.count_null_values())

class Plotter:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot_null_values(self):
        null_counts = self.dataframe.isnull().sum()
        null_counts.plot(kind='bar')
        plt.title('NULL Values in Columns')
        plt.xlabel('Columns')
        plt.ylabel('Count of NULL Values')
        plt.show()

plot = Plotter(df)
plot.plot_null_values()