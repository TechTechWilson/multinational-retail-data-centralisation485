import yaml
import psycopy2
import sqlalchemy 
from sqlalchemy import create_engine, inspect 

class DatabaseConnector:
    def __init__(self, yaml_file = 'db_creds.yaml'):
        self.yaml_file = yaml_file


    def read_db_creds(self):
        try:
            with open(self.yaml_file, 'r') as file:
                credentials = yaml.safe_load(file)
            return credentials
        except FileNotFoundError:
            print("Error: Credentials not found.")
        return None
    
    
def init_db_engine(self):
    
    db_creds = self.read_db_creds()
    if db_creds is not None:

        self.adapter = 'psycopy2'
        self.database_type = 'postgresql'
        self.password = db_creds['RDS_PASSWORD']
        self.host = db_creds['RDS_NAME']
        self.user = db_creds['RDS_USER']
        self.database = db_creds['RDS_DATABASE']
        self.port = db_creds['RDS_PORT']

        engine_url= f"{self.database_type}+{self.adapter}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        create = engine_engine(engine_url)
        return engine
    else:
        print("Error: No valid credentials found in yaml file.")
        return None

def list_db_tables(self):
    engine = self.init_db_engine()
    if engine is not None:
        try:
            insector = inspect(engine)
            return insector.get_table_names()
        except Exception as e:
            print(f"Error: {e}")
            return None

def upload_to_db(self, df, table_name):
        """
        Uploads a DataFrame to the database.
        """
        try:
            df.to_sql(table_name, self.db_engine, if_exists='replace', index=False)
            print(f"Data successfully uploaded to {table_name}")
        except Exception as e:
            print(f"Error uploading to database: {e}")


db_to_sql = clean_dataframe.to.sql(Table_name)
 if __name__ == "__main__":
    pass 

db_connector = DatabaseConnector()
tables = db_connector.list_db_tables()
print("Available tables:", {tables})
