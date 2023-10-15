import yaml
import sqlalchemy
import pandas as pd

def load_credentials():
    '''A function that gets the login/credential details in a yaml file that is stored securely'''
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

class RDSDatabaseConnector:
    '''Define a class that takes in the credential info from the previous function load_credentials()'''
    def __init__(self, credentials):
        self.credentials = credentials

    def create_engine(self):
        '''Define a create_engine function that allows you to extract data to the database'''
        from sqlalchemy import create_engine
        connection_str = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        self.engine = sqlalchemy.create_engine(connection_str)

    def extract_data(self):
        '''Extract data from the RDS database and return it as a panda dataframe'''
        query = "SELECT * FROM loan_payments"
        return pd.read_sql(query, self.engine)

def save_to_csv(dataframe, filename):
    '''Create a function that allows you to save the database locally'''
    dataframe.to_csv(filename, index=False)

if __name__ == "__main__":
    credentials = load_credentials()
    rds_connector = RDSDatabaseConnector(credentials)
    rds_connector.create_engine()
    data = rds_connector.extract_data()
    save_to_csv(data, "loan_payments.csv")