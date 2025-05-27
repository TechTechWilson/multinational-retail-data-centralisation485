from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

def run_pipeline():
    # Initialise connectors
    raw_db = DatabaseConnector("db_creds_raw.yaml")
    clean_db = DatabaseConnector("db_creds_clean.yaml")
    extractor = DataExtractor()
    cleaner = DataCleaning()

    # Products (S3)
    product_df = extractor.extract_from_s3("s3://data-handling-public/products.csv")
    cleaned_product_df = cleaner.clean_products_data(product_df)
    clean_db.upload_to_db(cleaned_product_df, "dim_products")

    # Stores (API)
    total_stores = extractor.list_number_of_stores()
    store_df = extractor.retrieve_all_stores_data(total_stores)
    cleaned_store_df = cleaner.clean_store_data(store_df)
    clean_db.upload_to_db(cleaned_store_df, "dim_store_details")

    # Orders (Raw DB)
    orders_df = raw_db.read_rds_table("orders_table")
    cleaned_orders_df = cleaner.clean_orders_data(orders_df)
    clean_db.upload_to_db(cleaned_orders_df, "orders_table")

    # Date Times (JSON S3)
    date_df = extractor.extract_json_from_s3("date_details.json")
    cleaned_date_df = cleaner.clean_date_times_data(date_df)
    clean_db.upload_to_db(cleaned_date_df, "dim_date_times")

if __name__ == "__main__":
    run_pipeline()
