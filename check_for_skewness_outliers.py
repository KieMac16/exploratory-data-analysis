'''This file has the following, used to visualise data

A QQ plot to determine skewness of specific columns
Box plots for numerical columns to identify outliers
Box plots after outlier are removed

'''

'''Relevant imports and the file path of the original data'''
# import matplotlib.pyplot as plt
# import pandas as pd
# import statsmodels.api as sm

# file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
# df = pd.read_csv(file_path)

'''QQ plot to check for skewness'''
# for column in df.columns:
#     sm.qqplot(df[column], line='s')
#     plt.title(f'QQ Plot for {column}')
#     plt.show()

'''I used a Plotter class from df_transform, also in this repo'''
# from df_transform import Plotter
# plot = Plotter(df)

'''I identified skewed columns individually'''
# skewed_columns = df[['loan_amount', 'funded_amount', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_rec_prncp', 'last_payment_amount']].skew()
# transform_df.transform_skewed_columns(skewed_columns)
# plot.plot_skewness(skewed_columns) # Visualise skewness

'''Save a copy of transformed data to a new file, to check the transformations'''
# df.to_csv('transformed__EDA_data.csv', index=False) # Save a copy to my directory

'''Box plots for before and after outliers are removed'''
# for column in df.select_dtypes(include=['number']).columns:
#    plt.figure(figsize=(8, 6))  # Set the figure size
#    plt.boxplot(df[column])  # Create the box plot
#    plt.title(f'Box Plot of {column}')  # Set the title
#    plt.xlabel('Value')  # X-axis label
#    plt.ylabel(column)  # Y-axis label
#    plt.show()

'''Outliers were chosen by identifying relevant columns from each individual box plot'''
# outlier_columns = df[['loan_amount', 'funded_amount', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']]
# remove_outliers = transform_df.remove_outliers(outlier_columns.columns, z_threshold=3)

'''Sense check with new box plots, which ultimately led to me restoring 3 columns'''
# for column in outlier_columns.columns:
#     plt.figure(figsize=(8, 6))
#     plt.boxplot(remove_outliers[column], showfliers=False)  # Set showfliers to False to remove outliers
#     plt.title(f'Box Plot of {column}')
#     plt.xlabel('Value')
#     plt.ylabel(column)
#     plt.show()