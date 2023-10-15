import pandas as pd

def load_data_from_csv(filename):
    '''A function that will load the first 5 rows of data and tell us the shape of the database'''
    try:
        dataframe = pd.read_csv(filename)
        print("Data Shape:", dataframe.shape) # print the number of rows and columns to understand the size of the database
        print("\nSample of the Data:")
        print(dataframe.head())
        return dataframe
    except FileNotFoundError: # Use an Error incase the file won't load
        print(f"File {filename} not found.")
        return None

if __name__ == "__main__":
    '''Ensure that the rest of the code can be used with other files but we will run the loan_payments.csv file if the function is called within this file'''
    filename = "C:/Users/kiera/KieMac/exploratory-data-analysis/loan_payments.csv"
    data = load_data_from_csv(filename)