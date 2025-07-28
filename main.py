import logging
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Configure logging for the pipeline
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def run_pipeline():
    raw_db = DatabaseConnector("db_creds_raw.yaml")
    clean_db = DatabaseConnector("db_creds_clean.yaml")
    extractor = DataExtractor()
    cleaner = DataCleaning()

    # Products (S3)
    try:
        logging.info("Starting product data extraction.")
        product_df = extractor.extract_from_s3("s3://data-handling-public/products.csv")
        cleaned_product_df = cleaner.clean_products_data(product_df)
        if cleaned_product_df.empty:
            logging.warning("Cleaned products DataFrame is empty. Skipping upload.")
        else:
            # Verify table name here matches your DB schema
            clean_db.upload_to_db(cleaned_product_df, "dim_product_details")
            logging.info("Products uploaded successfully.")
    except Exception as e:
        logging.error(f"Error processing products: {e}")

    # Stores (API)
    try:
        logging.info("Starting store data extraction.")
        total_stores = extractor.list_number_of_stores()
        store_df = extractor.retrieve_all_stores_data(total_stores)
        cleaned_store_df = cleaner.clean_store_data(store_df)
        if cleaned_store_df.empty:
            logging.warning("Cleaned stores DataFrame is empty. Skipping upload.")
        else:
            # Verify table name here matches your DB schema
            clean_db.upload_to_db(cleaned_store_df, "legacy_store_details")
            logging.info("Stores uploaded successfully.")
    except Exception as e:
        logging.error(f"Error processing stores: {e}")

    # Orders (Raw DB)
    try:
        logging.info("Starting orders data extraction.")
        orders_df = raw_db.read_rds_table("orders_table")
        cleaned_orders_df = cleaner.clean_orders_data(orders_df)
        if cleaned_orders_df.empty:
            logging.warning("Cleaned orders DataFrame is empty. Skipping upload.")
        else:
            clean_db.upload_to_db(cleaned_orders_df, "orders_table")
            logging.info("Orders uploaded successfully.")
    except Exception as e:
        logging.error(f"Error processing orders: {e}")

    # Date Times (JSON S3)
    try:
        logging.info("Starting date times data extraction.")
        date_df = extractor.extract_json_from_s3("date_details.json")
        cleaned_date_df = cleaner.clean_date_times_data(date_df)
        if cleaned_date_df.empty:
            logging.warning("Cleaned date times DataFrame is empty. Skipping upload.")
        else:
            # Verify table name here matches your DB schema
            clean_db.upload_to_db(cleaned_date_df, "dim_date_times")
            logging.info("Date times uploaded successfully.")
    except Exception as e:
        logging.error(f"Error processing date times: {e}")

if __name__ == "__main__":
    run_pipeline()
