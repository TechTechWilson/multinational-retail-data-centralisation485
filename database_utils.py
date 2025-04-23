print("database_utils.py loaded")

import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect


class DatabaseConnector:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.engine = None

    def read_db_creds(self):
        """
        Reads YAML file with database credentials.
        
        """
        try:
            with open(self.yaml_file, 'r') as file:
                creds = yaml.safe_load(file)
            return creds
        except Exception as e:
            print(f"Error reading YAML: {e}")
            return None

    def init_db_engine(self):
        """
        Initialises a SQLAlchemy engine based on the YAML credentials.

        """
        creds = self.read_db_creds()
        if creds:
            db_url = f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
            try:
                self.engine = create_engine(db_url)
                return self.engine
            except Exception as e:
                print(f"Failed to create engine: {e}")
                return None

    def list_db_tables(self):
        """
        Lists all tables in the connected database.
        
        """
        if self.engine is None:
            self.init_db_engine()

        if self.engine is not None:
            try:
                inspector = inspect(self.engine)
                return inspector.get_table_names()
            except Exception as e:
                print(f"Error inspecting database: {e}")
                return None

    def upload_to_db(self, df, table_name):
        """
        
        Uploads a DataFrame to the database.
        
        """
        if self.engine is None:
         self.init_db_engine()
         
        if self.engine is not None:
            self.init_db_engine()

        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Data successfully uploaded to {table_name}")
        except Exception as e:
            print(f"Error uploading to database: {e}")
        else;
            print("Database engine is not initialized. Please check your credentials.")

if __name__ == "__main__":
    connector = DatabaseConnector("db_creds.yaml")
    engine = connector.init_db_engine()
    tables = connector.list_db_tables()

    if engine and tables:
        print("Connected to the database!")
        print("Tables in DB:", tables)
    else:
        print("Could not connect to the database.")
