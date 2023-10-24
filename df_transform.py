import pandas as pd
import matplotlib.pyplot as plt # make sure you have .pyplot as matplotlib wouldn't plot my matrix
import plotly.express as px
import missingno as msno

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

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

transform_df = DataFrameTransform(df)

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
columns_to_drop = ['mths_since_last_delinq',
                   'mths_since_last_record',
                   'next_payment_date',
                   'mths_since_last_major_derog',
]
df.drop(columns_to_drop, axis=1, inplace=True)

columns_to_review = ['funded_amount', # 1122 distinct values
                     'term', # 2 distinct values
                     'int_rate', # 457 distinct values
                     'employment_length', # 11 distinct values
                     'last_payment_date', # fforward
                     'last_credit_pull_date' # fforward
                     'collections_12_mths_ex_med' # 5 distinct values
                     ]

'''I am going to explore the following columns further'''
# print(df['term'].unique()) # gives 36 and 60 months
# print(df['employment_length'].unique()) # gives 5, 6, 1, 10+ and <1
# print(df['collections_12_mths_ex_med'].unique()) # gives 0 1 2 3 4

'''Therefore I will forward fill the following columns'''
df['last_payment_date'].fillna(method='ffill', inplace=True)
df['collections_12_mths_ex_med'].fillna(method='ffill', inplace=True) # I chose this over mean/median intentionally
df['last_credit_pull_date'].fillna(method='ffill', inplace=True)

'''Finally I will use .describe with 3 columns to make a decision on mean/median and check the null rows head(10)'''
# print(df['funded_amount'].describe())
# print(df['int_rate'].describe())
# print(df['employment_length'].describe())
# rows_with_null = df[df.isnull().any(axis=1)].head(10)
# print(rows_with_null)

'''I am going to impute the following with the mean or median, however I need to clean the data for 2 columns in the main doc so have left them in #'''
transform_df.impute_missing('funded_amount','mean') # Need to investigate further with outliers
transform_df.impute_missing('int_rate','mean') # Very similar to the median
# transform_df.impute_missing('term','mean') # Only between 2 values
# transform_df.impute_missing('employment_length','mean') # Are not in the correct format

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