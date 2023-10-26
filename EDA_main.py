import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

from convert_column_formats import DataTransform
column_transform = DataTransform(df)

# Remove excess symbols from column(s) - I've made this but don't think I need it upon inspecting the data
column_transform.remove_excess_symbols('term','months')
df['employment_length'] = df['employment_length'].str.extract('(\d+)').astype(float)

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

'''This checks whether all columns have no NULL values, but the code has been commented out'''
# from get_info_from_df import DataFrameInfo
# df_info = DataFrameInfo(df)
# print(df_info.count_null_values()) # Generate a count of NULL values in each column

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
numeric_columns = df.select_dtypes(include=['number']) # Allows me to create a heatmap as I need numeric values
px.imshow(numeric_columns.corr(), title="Correlation Heatmap of the DF").show()

#The following columns had an heatmap rating greater than 0.85 with another column:
highly_correlated_columns = df[['member_id','funded_amount_inv','instalment','out_prncp_inv','total_payment_inv','total_rec_prncp',]]
df.drop(highly_correlated_columns, axis=1, inplace=True)

'''The following code will analyse the data and identify KPI and areas of interest'''
separator = '-' * 60 # Use this to separate different sections of information

# First, look at the total loan amounts funded by the bank against total payments recovered and print
total_funded = df['funded_amount'].sum()
total_received = df['total_payment'].sum()
percentage_recovery = (total_received / total_funded) * 100

print(separator)
print('LOAN RECOVERIES')
print(f"Total Amount Funded: ${total_funded:.0f}")
print(f"Total Amount Received: ${total_received:.0f}")
print(f"Percentage Recovered: {percentage_recovery:.1f}%")

'''
I checked to see if the lowest issue date for 'current' loans is within the 'term' time using the code that is commented out below. 
It's very likely the recovery projection is an overestimate.
This is because I couldn't get the remaining months (1-6) for 'Current' loans.
Some loans may only have 1 month left until full payment and I counted 6.
'''
current_loans = df[df['loan_status'] == 'Current']
# lowest_issue_date = current_loans['issue_date'].min().strftime('%b-%Y')
# print(lowest_issue_date)

projection_month = 6
total_projected_amount = (current_loans['last_payment_amount'] * projection_month).sum()
total_after_projection = total_received + total_projected_amount
percentage_received_6_months = (total_after_projection / total_funded) * 100
print(separator)
print('PROJECTIONS')
print(f"Total amount projected to recover after {projection_month} months: ${total_projected_amount:.0f}")
print(f"Total projected percentage recovered after {projection_month} months: {percentage_received_6_months:.1f}%")


'''I used a search engine to get me some code to produce data visualisations:

I went for a bar chart for obvious reasons.
I looked at a speedometer style visualisation for percentages but it didn't look good.
Taking this data into SQL or Power BI would be a preferred next step to work better with cleaned data.
'''
categories = ['Received', 'Funded', 'Projected']
values = [total_received,total_funded,total_after_projection]

# Create a bar chart to visualise the 3 categories
plt.figure(figsize=(8, 6))
plt.bar(categories, values, color=['black','red','blue'])
plt.title('Received v Funded v Projected')
plt.ylabel('Amount $')
plt.show()

'''Now I want to look at the loans that have been charged off - recorded as loss from the company'''
charged_off_loans = df[df['loan_status'] == 'Charged Off'] # Filter to charged off
total_loans = len(df)
charged_off_count = len(charged_off_loans)
charged_off_percentage = (charged_off_count / total_loans) * 100
total_charged_off_payments_received = charged_off_loans['total_payment'].sum()

print(separator)
print('CHARGED OFF LOANS')
print(f"Percentage of charged-off loans: {charged_off_percentage:.1f}%")
print(f"Total amount paid towards charged-off loans: ${total_charged_off_payments_received:.0f}")

'''Next I will look at the revenue loss from charged off loans'''
# # I've decided to define a function to calculate projected revenue for each loan type
def calculate_projected_revenue(row):
    monthly_interest_rate = (row['int_rate'] / 100) / 12
    num_payments = row['term']
    # Now use the "Monthly Payment Formula" to find projected revenue
    projected_revenue = row['funded_amount'] * (monthly_interest_rate * ((1 + monthly_interest_rate) ** num_payments)) / (((1 + monthly_interest_rate) ** num_payments) - 1)
    return projected_revenue

'''I'm interested to see projections, including interest, of charged_off and current loans

We need the projections, including interest, for charged off loans to determine what the company is potentially losing.
I've inlcuded the projections of current loans, although this isn't needed right now, so I've commented it out.
This could be a next step to look at net income.
'''
# The filters for current_loans and charged_off_loans are defined previously
charged_off_loans = charged_off_loans.copy()  # Create a copy of the DataFrame to solve an Error raised
charged_off_loans['projected_revenue'] = charged_off_loans.apply(lambda row: calculate_projected_revenue(row), axis=1)
total_projected_loss_charged_off = charged_off_loans['projected_revenue'].sum()

# current_loans['projected_revenue'] = current_loans.apply(calculate_projected_revenue, axis=1) # Now project revenue from current loans
# total_projected_income_current = current_loans['projected_revenue'].sum()

percentage_revenue_loss = (total_projected_loss_charged_off / total_funded) * 100

print(separator)
print('REVENUE LOSS FROM CHARGED OFF LOANS')
print(f"Total Projected Revenue Loss for charged off loans: ${total_projected_loss_charged_off:.0f}")
print(f"Percentage of Expected Revenue Lost from charged off loans: {percentage_revenue_loss:.1f}%")

'''Now I will look at customers who are a risk to the company'''
# First, I want to check all of the loan_status options and determine which of these present a risk (code commented out)
# loan_status = df['loan_status'].unique()
# print(loan_status) # There are two late statuses and a default. For now I will leave the grace period out of the analysis

# Apply a filter for my at_risk loans, and produce a count to print and percentage of overall loans
at_risk_loans = df[df['loan_status'].isin(['Late (31-120 days)', 'Late (16-30 days)', 'Default'])]
at_risk_loans_count = len(at_risk_loans)
at_risk_loans_percentage = (at_risk_loans_count/total_loans) * 100

 # Run at_risk_loans through the previously defined function calculate_projected_revenue
at_risk_loans = at_risk_loans.copy()  # Create a copy as before to resolve an Error
at_risk_loans['projected_revenue'] = at_risk_loans.apply(lambda row: calculate_projected_revenue(row), axis=1)
total_projected_loss_at_risk = at_risk_loans['projected_revenue'].sum()

print(separator)
print('AT RISK LOANS')
print(f"The total amount of customers who are at risk: {at_risk_loans_count}")
print(f"The percentage of total customers who are at risk: {at_risk_loans_percentage:.1f}%")
print(f"Total Projected Revenue Loss for at risk loans: ${total_projected_loss_at_risk:.0f}")

''' If the group of at_risk were combined with charged off, we can work out the total revenue loss as a percentage'''
at_risk_charged_off_revenue = total_projected_loss_charged_off + total_projected_loss_at_risk
at_risk_charged_off_percentage = at_risk_charged_off_revenue / total_funded * 100

print(separator)
print("AT RISK AND CHARGED OFF")
print(f"The total amount of revenue loss for at risk and charged off loans: ${at_risk_charged_off_revenue:.0f}")
print(f"This represents a possible percentage revenue loss of: {at_risk_charged_off_percentage:.1f}%")

'''Finally, determine factors that may be indicators of loss to influence future decisions'''

'''First I will look at a correlation matrix for both subsets (at risk and charged off)
I initially did this on the same plot but it was difficult to read so opted for separate plots.
The startling thing when doing this was the employment_length had 0 entries, so this allowed me to fix that.
I also think the measure projected_revenue shows strong correlation in both diagrams, so will investigate
'''
numerical_columns_at_risk = at_risk_loans.select_dtypes(include=['number'])
numerical_columns_charged_off = charged_off_loans.select_dtypes(include=['number'])

correlation_matrix_at_risk = numerical_columns_at_risk.corr() # Compute the correlation matrix for at_risk
correlation_matrix_charged_off = numerical_columns_charged_off.corr() # Compute the correlation matrix for charged_off

# Create plot for at_risk
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix_at_risk, annot=True, cmap='coolwarm', fmt=".2f")

plt.title("Correlation Matrix - At-Risk Loans")
plt.show()

# Create a plot for charged off
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix_charged_off, annot=True, cmap='coolwarm', fmt=".2f")

plt.title("Correlation Matrix - Charged-Off Loans")
plt.show()

'''Then, I will look at creating bar charts to compare the 'grades' for both subsets at_risk and charged_off'''
grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Define the order of grades

X = np.arange(len(grades))

# Extract the counts for at-risk and charged-off loans for each grade
at_risk_counts_grade = at_risk_loans['grade'].value_counts().reindex(grades, fill_value=0)
charged_off_counts_grade = charged_off_loans['grade'].value_counts().reindex(grades, fill_value=0)

# Define colours for consistency
at_risk_color = '#36454F'
charged_off_color = '#DC143C'

# Create the bar chart
bar_width = 0.4  # Adjust the bar width as needed
plt.bar(X - bar_width/2, at_risk_counts_grade, bar_width, label='At-Risk Loans', color = at_risk_color)
plt.bar(X + bar_width/2, charged_off_counts_grade, bar_width, label='Charged-Off Loans', color = charged_off_color)

plt.xticks(X, grades)
plt.xlabel("Grades")
plt.ylabel("Number of Loans")
plt.title("Number of At-Risk and Charged-Off Loans by Grade")
plt.legend()
plt.show()

'''I didn't like the previous chart so instead I changed the axis to look at proportion and make the graphs more comparable'''

fig, ax1 = plt.subplots() # Create the figure with two subplots sharing the x-axis

# Create the first bar chart for 'at_risk' with the primary y-axis
ax1.bar(X - 0.2, at_risk_counts_grade, 0.4, label='At-Risk Loans', color=at_risk_color)
ax1.set_xlabel("Grades")
ax1.set_ylabel("Count (At-Risk Loans)", color=at_risk_color)
ax1.tick_params(axis='y', labelcolor=at_risk_color)
ax1.set_xticks(X)
ax1.set_xticklabels(grades)

# Create a secondary y-axis for the second bar chart for 'charged_off'
ax2 = ax1.twinx()
ax2.bar(X + 0.2, charged_off_counts_grade, 0.4, label='Charged-Off Loans', color=charged_off_color)
ax2.set_ylabel("Count (Charged-Off Loans)", color=charged_off_color)
ax2.tick_params(axis='y', labelcolor=charged_off_color)

# Add a legend for both datasets
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.85))

plt.title("Comparison of Counts of At-Risk and Charged-Off Loans by Grade")
plt.show()

'''Now, I am going to repeat the dual bar chart for the 'purpose' column.'''
# print(df['purpose'].unique()) # Use this to define the purpose columns
purpose = ['credit_card','debt_consolidation','home_improvement','small_business','renewable_energy' 'major_purchase' 'other' 'moving' 'car' 'medical','house','vacation','wedding','educational']
X = np.arange(len(purpose))

# Extract the counts for at-risk and charged-off loans for each grade
at_risk_counts_purpose = at_risk_loans['purpose'].value_counts().reindex(purpose, fill_value=0)
charged_off_counts_purpose = charged_off_loans['purpose'].value_counts().reindex(purpose, fill_value=0)

fig, ax1 = plt.subplots() # Create the figure with two subplots sharing the x-axis

plt.xticks(X, purpose, rotation=70, fontsize=6)  # Rotate the labels by 90 degrees

# Create the first bar chart for 'at_risk' with the primary y-axis
ax1.bar(X - 0.2, at_risk_counts_purpose, 0.4, label='At-Risk Loans', color=at_risk_color)
ax1.set_xlabel("Purpose")
ax1.set_ylabel("Count (At-Risk Loans)", color=at_risk_color)
ax1.tick_params(axis='y', labelcolor=at_risk_color)
ax1.set_xticks(X)
ax1.set_xticklabels(purpose)

# Create a secondary y-axis for the second bar chart for 'charged_off'
ax2 = ax1.twinx()
ax2.bar(X + 0.2, charged_off_counts_purpose, 0.4, label='Charged-Off Loans', color=charged_off_color)
ax2.set_ylabel("Count (Charged-Off Loans)", color=charged_off_color)
ax2.tick_params(axis='y', labelcolor=charged_off_color)

# Add a legend for both datasets
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.85))

plt.title("Comparison of Counts of At-Risk and Charged-Off Loans by Grade")
plt.show()

'''Next, I will look at the debt-to-income (dti) ratio, to gauge whether this has had an impact on repayments'''

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# First subplot for 'at_risk_loans'
sns.histplot(data=at_risk_loans, x=at_risk_loans['dti'], kde=True, ax=axes[0], color=at_risk_color)
axes[0].set_xlabel('DTI')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of DTI - At Risk Loans')

# Second subplot for 'charged_off_loans'
sns.histplot(data=charged_off_loans, x=charged_off_loans['dti'], kde=True, ax=axes[1], color=charged_off_color)
axes[1].set_xlabel('DTI')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution of DTI - Charged Off Loans')

# Adjust layout and show the figure
plt.tight_layout()
plt.show()

'''And finally, projected revenue which was a measure flagged from the correlation matrix'''

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# First subplot for 'at_risk_loans'
sns.histplot(data=at_risk_loans, x=at_risk_loans['projected_revenue'], kde=True, ax=axes[0], color=at_risk_color)
axes[0].set_xlabel('Projected Revenue')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Projected Revenue - At Risk Loans')

# Second subplot for 'charged_off_loans'
sns.histplot(data=charged_off_loans, x=charged_off_loans['projected_revenue'], kde=True, ax=axes[1], color=charged_off_color)
axes[1].set_xlabel('Projected Revenue')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution of Projected Revenue - Charged Off Loans')

# Adjust layout and show the figure
plt.tight_layout()
plt.show()

'''An analysis shows the following risk factors:
'''
print(separator)
print('Grades: There is a clear correlation between grades B, C, D and E for Charged Off Loans and this trend is continuing with At Risk.')
print(separator)
print('Purpose: Credit Card and Debt Consolidation loans are significantly contributing to revenue loss.')
print('Home improvement and Small Business are also factors to consider.')
print(separator)
print('DTI: Whilst the curves arent perfectly similar, the tip of both distributions are centred.')
print('These values range from 8 to 25, with numbers either side of this relatively low in the distribution.')
print(separator)
print('Whilst projected revenue is a created measure, it shows the projected revenue between $200-500k is significant for non-repayment issues.')
