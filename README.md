# EDA Customer Loans in Finance

### 1. [The Project](#PD)
### 2. [Installation Instructions](#II)
### 3. [File Structure](#FS)
### 4. [Data Files](#LI)
-------------------------------------------
## The Project: <a name="PD"></a>

This is a data analysis project that takes a large dataset with 54,231 customers and 43 columns of data.
The ultimate goal is to review the state of the loans, consider loss and projected loss, and identify indicators of loss to learn from and influence future decisions.

The project had three significant steps:
1. Exctract the loans data
1. Clean the data
1. Analysis and visualisations

## Installation Instructions: <a name="II"></a>

This project was created on VSCode, using a Windows machine. I had downloaded Python from the extensions and ensured my environment was able to install using 'pip' commands.

To use all features within these files, you will need to install to run the following:

- import matplotlib.pyplot as plt
- import missingno as msno
- import numpy as np
- import pandas as pd
- import plotly.express as px
- import seaborn as sns
- import statsmodels.api as sm

You may need to install the programmes to your environment, which is likely as easy as typing 'pip install numpy' into your terminal, depending on your OS.

**The main file which can be run with loan_payments.csv is eda_main.py**

Other files have been used to build this, and a short explanation is provided in the File Structure section below.

## File Structure: <a name="FS"></a>
- #### Credentials (credentials.yaml)
Contains the credentials that allowed me to download the data from a server.
- #### Getting the data (db_utils)
Create a class that extracts data and returns it as a panda df. Define functions that will open the credentials document for data extraction and another function so save the extracted data as a csv.
- #### Which files to push to GitHub
Ensure a gitignore file is created to withold credential information from GitHub.
- #### Load Loan Payments (load_loan_payments)
Get familiar with the data shape - by loading some of the data and thinking about possible next steps or areas of interest.
- #### Check Data Types (check_data_types)
Use the .dtypes to further inspect the data and think of next steps.
- #### Become familiar with the DataFrme (get_info_from_df)
Identify null values and percentage of null values, so that key columns are identified for the data cleaning process.
Identify distinct values to consider any boolean columns and any categorical columns.
- #### Ensure Columns are in the correct format (convert_column_formats)
class DataTransform
After inspecting the data a decision has been made to convert columns to categorical, numerical, boolean or date format. Also, removing symbols from identified columns to allow these to be converted to numerical for analysis.

*The decisions made were finalised in the eda_main file, with the class called in that document.*
- #### Transform the data (df_transform)
class DataFrameTransform
This was used to identify columns to drop, fill forward and impute using either the mean or median.
class Plotter
This was used to inform decisions made by plotting null values and skewness.

*The decisions made were finalised in the eda_main file, with the class called in that document.*
- #### Skewness and Outliers (check_for_skewness_outliers)
To reduce the length of code, I have stored the code used to analyse the data using the Plotter class in a separate file. 
QQ plot.
Boxplot.
For me, it was important to visualise these by column rather than using code to determine outliers and skewness so I could make a decision with the context of each column.
- #### Full code (EDA_main)
This code runs well and produces specific charts that allows informed decisions to be made regarding loan repayments, projected loss, factors affecting loss and future decisions to make.

The code runs in the following order:
- Load the data from loan_payments.csv
- Use the DataTransform class to ensure all columns are in the correct format to allow analysis
- Use the DataFrameTransform class to drop specific columns and clean up others (impute, fill forward), based on null values
- Use the Plotter class to check for skewness and outliers and identify any columns to transform 
- An analysis, with diagrams, that calculated:

The current state of the loans  
Calculating loss  
Projected loss  
Possible loss  
Indicators of loss  

##### License Information:  <a name="LI"></a>
