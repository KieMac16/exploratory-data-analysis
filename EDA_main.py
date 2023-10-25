import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

df.info()

from convert_column_formats import DataTransform
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

from df_transform import DataFrameTransform
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

'''This checks whether all columns have no NULL values'''
from get_info_from_df import DataFrameInfo
df_info = DataFrameInfo(df)

'''Now I will use the Plotter Class to continue with analysis, looking at skewness and outliers'''
from df_transform import Plotter
plot = Plotter(df)

'''I used a QQ Graph in check_for_skewness_outliers.py to determine the following columns to transform:'''
skewed_columns = df[['loan_amount', 'funded_amount', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_rec_prncp', 'last_payment_amount']].skew()
transform_df.transform_skewed_columns(skewed_columns) # Transforms the skewed columns, using a graph after the transformation to ensure it has

'''I used a series of box plots in check_for_skewness_outliers to determine the following columns to transform:'''
outlier_columns = df[['loan_amount', 'funded_amount', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']]
remove_outliers = transform_df.remove_outliers(outlier_columns.columns, z_threshold=3) # Removed outliers
'''After I removed outliers, I used the box plots to determine 3 columns to remove from my outlier_columns list as the box plots were centred at 0'''

'''Create a heatmap of the numerical columns to inspect and decide on further columns to drop'''
# numeric_columns = df.select_dtypes(include=['number']) # Allows me to create a heatmap as I need numeric values
# px.imshow(numeric_columns.corr(), title="Correlation Heatmap of the DF").show()

#The following columns had an heatmap rating greater than 0.85 with another column:
highly_correlated_columns = df[['member_id','funded_amount','funded_amount_inv','instalment','out_prncp_inv','total_payment_inv','total_rec_prncp',]]
df.drop(highly_correlated_columns, axis=1, inplace=True)

df.info()