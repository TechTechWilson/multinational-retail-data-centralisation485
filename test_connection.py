print("test_connection.py IS RUNNING")

from database_utils import DatabaseConnector

print("Imported DatabaseConnector")

if __name__ == "__main__":
    print("Initialising DatabaseConnector...")
    connector = DatabaseConnector("db_creds.yaml")
    engine = connector.init_db_engine()

    if engine:
        print("Connected to AWS RDS successfully.")
        print("Tables:", connector.list_db_tables())
    else:
        print("Connection failed.")
