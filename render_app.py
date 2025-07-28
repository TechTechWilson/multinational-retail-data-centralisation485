from flask import Flask, jsonify
import logging
import os
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Multinational Retail Data Centralization",
        "version": "1.0.0"
    })

@app.route('/run-etl')
def run_etl():
    try:
        # Use environment variables for database connection
        clean_db = DatabaseConnector("production")  # We'll modify this to use env vars
        extractor = DataExtractor()
        cleaner = DataCleaning()
        
        results = {
            "status": "success",
            "processed_tables": []
        }
        
        # Products (S3)
        try:
            product_df = extractor.extract_from_s3("s3://data-handling-public/products.csv")
            cleaned_product_df = cleaner.clean_products_data(product_df)
            if not cleaned_product_df.empty:
                clean_db.upload_to_db(cleaned_product_df, "dim_products")
                results["processed_tables"].append("dim_products")
        except Exception as e:
            results[f"error_products"] = str(e)

        # Stores (API)
        try:
            total_stores = extractor.list_number_of_stores()
            if total_stores:
                store_df = extractor.retrieve_all_stores_data(total_stores)
                cleaned_store_df = cleaner.clean_store_data(store_df)
                if not cleaned_store_df.empty:
                    clean_db.upload_to_db(cleaned_store_df, "dim_store_details")
                    results["processed_tables"].append("dim_store_details")
        except Exception as e:
            results[f"error_stores"] = str(e)

        # Date Times (JSON S3)
        try:
            date_df = extractor.extract_json_from_s3("date_details.json")
            cleaned_date_df = cleaner.clean_date_times_data(date_df)
            if not cleaned_date_df.empty:
                clean_db.upload_to_db(cleaned_date_df, "dim_date_times")
                results["processed_tables"].append("dim_date_times")
        except Exception as e:
            results[f"error_date_times"] = str(e)
            
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/tables')
def list_tables():
    try:
        clean_db = DatabaseConnector("production")
        tables = clean_db.list_db_tables()
        return jsonify({
            "status": "success",
            "tables": tables
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 