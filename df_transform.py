# import pandas as pd
# import matplotlib.pyplot as plt # make sure you have .pyplot as matplotlib wouldn't plot my matrix
# import plotly.express as px
# import missingno as msno
import numpy as np

# file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
# df = pd.read_csv(file_path)

'''The DataFrameTransform Class and Plotter Class is used in the EDA_main but I developed it in this file'''

class DataFrameTransform:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def count_null_values(self): #A function that will count null values per column in the df
        return self.dataframe.isnull().sum()
    
    def impute_missing(self, column_name, impute_with='mean'):
        '''A loop will allow me to choose between the mean, median and mode for imputing columns with NaN'''
        if impute_with == 'mean':
            self.dataframe[column_name].fillna(self.dataframe[column_name].mean(), inplace=True)
        elif impute_with == 'median':
            self.dataframe[column_name].fillna(self.dataframe[column_name].median(), inplace=True)
        elif impute_with == 'mode':
            self.dataframe[column_name].fillna(self.dataframe[column_name].mode(), inplace=True)
        else:
            ValueError #Need a ValueError if the data isn't suitable for an average

    def transform_skewed_columns(self, columns):
        '''Use the following code for a log transforamtion'''
        for col in columns:
            if col in self.dataframe.columns:
                self.dataframe[col] = np.log1p(self.dataframe[col])

    def remove_outliers(self, columns, z_threshold=3):
        '''Ensure the following code is used on numerical columns, the Z score can be determined in the main coding and is variable'''
        for column_name in columns:
            z_scores = np.abs((self.dataframe[column_name] - self.dataframe[column_name].mean()) / self.dataframe[column_name].std())
            outliers = z_scores > z_threshold
            self.dataframe = self.dataframe[~outliers]
        return self.dataframe

# transform_df = DataFrameTransform(df)

# print(transform_df.count_null_values()) - I don't need this here anymore, will use in later code

'''I used plotly as px to look through different plots (histograms, scattergraphs) of my null valued columns'''
# fig = px.scatter(df,'last_payment_date')
# fig.show()

'''I used msno and plt to plot a matrix that checks all data input/missing values '''
#def plot_missing_data_matrix(df):
#    msno.matrix(df)
#    plt.show()

# plot_missing_data_matrix(df)

'''Now I am ready to drop the following columns'''
#columns_to_drop = ['mths_since_last_delinq',
#                   'mths_since_last_record',
#                   'next_payment_date',
#                   'mths_since_last_major_derog',
#]
#df.drop(columns_to_drop, axis=1, inplace=True)

#columns_to_review = ['funded_amount', # 1122 distinct values
#                     'term', # 2 distinct values
#                     'int_rate', # 457 distinct values
#                     'employment_length', # 11 distinct values
#                     'last_payment_date', # fforward
#                     'last_credit_pull_date' # fforward
#                     'collections_12_mths_ex_med' # 5 distinct values
#                     ]

'''I am going to explore the following columns further'''
# print(df['term'].unique()) # gives 36 and 60 months
# print(df['employment_length'].unique()) # gives 5, 6, 1, 10+ and <1
# print(df['collections_12_mths_ex_med'].unique()) # gives 0 1 2 3 4

'''Based on analysis in df_transform.py I will forward fill the following columns'''
#df['last_payment_date'].fillna(method='ffill', inplace=True)
#df['collections_12_mths_ex_med'].fillna(method='ffill', inplace=True) # I chose this over mean/median intentionally
#df['last_credit_pull_date'].fillna(method='ffill', inplace=True)

'''Finally I will use .describe with 3 columns to make a decision on mean/median and check the null rows head(10)'''
# print(df['funded_amount'].describe())
# print(df['int_rate'].describe())
# print(df['employment_length'].describe())
# rows_with_null = df[df.isnull().any(axis=1)].head(10)
# print(rows_with_null)

#'''I am going to impute the following with the mean or median'''
#transform_df.impute_missing('funded_amount','median') # Need to investigate further with outliers
#transform_df.impute_missing('int_rate','mean') # Very similar to the median
#transform_df.impute_missing('term','mean') # Only between 2 values
#transform_df.impute_missing('employment_length','median') #Needs a column transformation to work

#print(transform_df.count_null_values())

class Plotter:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def plot_null_values(self):
        '''A method that enables me to plot null values and continue to call until I had eliminated all null value columns'''
        null_counts = self.dataframe.isnull().sum()
        null_counts.plot(kind='bar')
        plt.title('NULL Values in Columns')
        plt.xlabel('Columns')
        plt.ylabel('Count of NULL Values')
        plt.show()
    
    def plot_skewness(self, skewness):
        '''A method that enables me to plot skewness, this was used before and after a transformation to ensure it worked'''
        skewness.plot(kind='bar')
        plt.title('Skewness of Columns')
        plt.xlabel('Columns')
        plt.ylabel('Skewness')
        plt.show()

# plot = Plotter(df)
#plot.plot_null_values()