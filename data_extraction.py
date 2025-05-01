import os
from io import StringIO
import boto3
import pandas as pd
import requests
import logging

logger = logging.getLogger(__name__)
from dotenv import load_dotenv

class DataExtractor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.num_stores_url = os.getenv("NUM_STORES_URL")
        self.store_url = os.getenv("STORE_DETAILS_URL")
        self.s3_bucket = os.getenv("S3_BUCKET_NAME")
        self.s3_object_key = os.getenv("S3_OBJECT_KEY")
        self.headers = {"x-api-key": self.api_key}

    def list_number_of_stores(self):
        try:
            response = requests.get(self.num_stores_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("number_stores")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get number of stores: {e}")
            raise

    def retrieve_store_data(self, store_number):
        """Fetch details for a specific store using its number."""
        url = f"{self.store_url}{store_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def retrieve_all_stores_data(self, total_stores):
        """Loop through store numbers to extract each store’s data."""
        all_stores = []
        for store_num in range(total_stores):
            store_data = self.retrieve_store_data(store_num)
            all_stores.append(store_data)
        return pd.DataFrame(all_stores)

    def extract_from_s3(self):
        """Pulls a CSV file from S3 and returns it as a pandas DataFrame."""
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=self.s3_bucket, Key=self.s3_object_key)
        data = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(data))
        return df
