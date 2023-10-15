import yaml
import sqlalchemy
import pandas as pd

def load_credentials():
    with open('credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials

    def create_engine(self):
        connection_str = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        self.engine = sqlalchemy.create_engine(connection_str)

    def extract_data(self):
        query = "SELECT * FROM loans_payments"
        return pd.read_sql(query, self.engine)

def save_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)

if __name__ == "__main__":
    credentials = load_credentials()
    rds_connector = RDSDatabaseConnector(credentials)
    rds_connector.create_engine()
    data = rds_connector.extract_data()
    save_to_csv(data, "loans_payments.csv")