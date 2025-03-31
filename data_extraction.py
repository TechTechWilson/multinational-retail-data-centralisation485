import boto3
from io import StringIO
import pandas as pd
import requests
import tabula  
import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from database_utils import DatabaseConnector

load_dotenv()

class DataExtractor:
    def __init__(self):

        self.api_key = os.getenv("API_KEY")
        self.num_stores_url = os.getenv("NUM_STORES_URL")
        self.store_url = os.getenv("STORE_DETAILS_URL")
        self.s3_bucket = os.getenv("S3_BUCKET_NAME")
        self.s3_object_key = os.getenv("S3_OBJECT_KEY")
        self.headers = {"x-api-key": self.api_key}
        self.db_connector = DatabaseConnector()

    def retrieve_pdf_data(self, pdf_url):
        pdf_dataframes = tabula.read_pdf(pdf_url, pages="all", multiple_tables=True)
        return pd.concat(pdf_dataframes, ignore_index=True)
    
    def read_rds_table(self, table_name: str):
        try:        
            engine = self.db_connector.init_db_engine()
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if table_name not in tables:
                return pd.DataFrame()
            
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql(query, engine)
        except Exception as e:
            print(f"Error reading table {table_name}: {e}")
            return pd.DataFrame()

    def list_number_of_stores(self):
        response = requests.get(self.num_stores_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("number_of_stores", 0)
        else:
            raise Exception(f"Failed to retrieve number of stores. Status code: {response.status_code}, {response.text}")
    
    def extract_from_s3(self):
        s3_client = boto3.client('s3') 
        response = s3_client.get_object(Bucket=self.s3_bucket, Key=self.s3_object_key)
        data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(data))
        return df

if __name__ == "__main__":
    extractor = DataExtractor()
    print("Environment variables loaded successfully.")
