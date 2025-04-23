from data_extraction import DataExtractor
from database_utils import DatabaseConnector

def test_list_number_of_stores(extractor):
    try:
        num_stores = extractor.list_number_of_stores()
        print(f"Number of stores returned: {num_stores}")
        assert isinstance(num_stores, int) and num_stores > 0, "Unexpected number of stores value"
    except Exception as e:
        print(f"[ERROR] list_number_of_stores() failed: {e}")

def test_extract_from_s3(extractor):
    try:
        df = extractor.extract_from_s3()
        print(f"Data extracted from S3 (first 5 rows):\n{df.head()}")
        assert not df.empty, "DataFrame from S3 is empty"
        assert "card_number" in df.columns, "Expected column 'card_number' missing"
    except Exception as e:
        print(f"[ERROR] extract_from_s3() failed: {e}")

if __name__ == "__main__":
    db_connector = DatabaseConnector('db_creds.yaml')
    extractor = DataExtractor(db_connector)

    print("Running tests...\n")
    
    test_list_number_of_stores(extractor)
    print()
    test_extract_from_s3(extractor)
