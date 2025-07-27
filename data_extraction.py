import os
from io import StringIO
import boto3
import pandas as pd
import requests
import logging
import json

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
        """Loop through store numbers to extract each store's data."""
        all_stores = []
        for store_num in range(total_stores):
            store_data = self.retrieve_store_data(store_num)
            all_stores.append(store_data)
        return pd.DataFrame(all_stores)

    def extract_from_s3(self, s3_path):
        try:
            s3 = boto3.client("s3")
            bucket, key = s3_path.replace("s3://", "").split("/", 1)
            obj = s3.get_object(Bucket=bucket, Key=key)
            data = obj["Body"].read().decode("utf-8")
            return pd.read_csv(StringIO(data))
        except Exception as e:
            logger.error(f"Error extracting from S3 {s3_path}: {e}")
            return pd.DataFrame()

    def extract_json_from_s3(self, json_file_name: str) -> pd.DataFrame:
        """
        Extracts JSON data from an S3 bucket and converts it to a pandas DataFrame.
        
        Args:
            json_file_name (str): The name of the JSON file in the S3 bucket
            
        Returns:
            pd.DataFrame: The extracted data as a pandas DataFrame
            
        Raises:
            Exception: If there's an error accessing the S3 bucket or processing the JSON data
        """
        try:
            s3 = boto3.client("s3")
            bucket = "public-data-handling-bucket"
            obj = s3.get_object(Bucket=bucket, Key=json_file_name)
            data = obj["Body"].read().decode("utf-8")
            json_data = json.loads(data)
            return pd.DataFrame(json_data)
        except Exception as e:
            logger.error(f"Error extracting JSON from S3 {json_file_name}: {e}")
            return pd.DataFrame()


