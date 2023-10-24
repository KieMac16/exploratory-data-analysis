import pandas as pd

file_path = 'C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv'
df = pd.read_csv(file_path)

class DataTransform:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_to_numeric(self, column_name):
        self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name], errors='coerce')

    def convert_to_date(self, column_name, date_format='%Y-%m-%d'):
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format=date_format, errors='coerce')

    def make_categorical(self, column_name):
        self.dataframe[column_name] = self.dataframe[column_name].astype('category')

    def convert_to_boolean(self, column_name, true_values=['y'], false_values=['n']):
        self.dataframe[column_name] = self.dataframe[column_name].isin(true_values)

    def remove_excess_symbols(self, column_name, symbol_to_remove):
        self.dataframe[column_name] = self.dataframe[column_name].str.replace(symbol_to_remove, '')
        
data_transformer = DataTransform(df)

# Convert column(s) to numerical format
data_transformer.convert_to_numeric('mths_since_last_delinq')
data_transformer.convert_to_numeric('mths_since_last_record')

# Convert column(s) to date format
data_transformer.convert_to_date('issue_date', date_format='%Y-%m')
data_transformer.convert_to_date('earliest_credit_line', date_format='%Y-%m')
data_transformer.convert_to_date('last_payment_date', date_format='%Y-%m')
data_transformer.convert_to_date('next_payment_date', date_format='%Y-%m')
data_transformer.convert_to_date('last_credit_pull_date', date_format='%Y-%m')

# Convert column(s) to categorical
data_transformer.make_categorical('term')
data_transformer.make_categorical('grade')
data_transformer.make_categorical('sub_grade')
data_transformer.make_categorical('employment_length')
data_transformer.make_categorical('home_ownership')
data_transformer.make_categorical('verification_status')
data_transformer.make_categorical('loan_status')
data_transformer.make_categorical('application_type')

# Convert column(s) to boolean:
data_transformer.convert_to_boolean('payment_plan')

# Remove excess symbols from column(s) - I've made this but don't think I need it upon inspecting the data
# data_transformer.remove_excess_symbols('','')