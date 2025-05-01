import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnector:
    def __init__(self, yaml_file, reinit=False):
        """
        Initialises the DatabaseConnector with a path to the YAML credentials file.
        """
        self.yaml_file = yaml_file
        self.engine = None
        if reinit:
            self.init_db_engine()

    def read_db_creds(self):
        """
        Reads YAML file with database credentials.
        
        Returns:
            dict: Database credentials.
        """
        try:
            with open(self.yaml_file, 'r') as file:
                creds = yaml.safe_load(file)
            required_keys = ['RDS_USER', 'RDS_PASSWORD', 'RDS_HOST', 'RDS_PORT', 'RDS_DATABASE']
            for key in required_keys:
                if key not in creds:
                    raise ValueError(f"Missing {key} in credentials file.")
            return creds
        except Exception as e:
            logger.error(f"Error reading YAML: {e}")
            return None

    def init_db_engine(self):
        """
        Initializes a SQLAlchemy engine using the database credentials.
        
        Returns:
            sqlalchemy.engine.Engine: SQLAlchemy engine object.
        """
        creds = self.read_db_creds()
        if creds:
            db_url = f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
            try:
                self.engine = create_engine(db_url)
                return self.engine
            except Exception as e:
                logger.error(f"Failed to create engine: {e}")
                return None
        else:
            logger.error("Credentials not found, cannot initialise database engine.")
            return None

    def list_db_tables(self):
        """
        Lists all the tables in the database.
        
        Returns:
            list: List of table names.
        """
        if self.engine:
            try:
                inspector = inspect(self.engine)
                return inspector.get_table_names()
            except Exception as e:
                logger.error(f"Error listing tables: {e}")
                return []
        else:
            logger.error("Database engine not initialised.")
            return []

    def read_rds_table(self, table_name):
        """
        Reads a table from the RDS database into a pandas DataFrame.
        
        Args:
            table_name (str): The table to fetch.
        
        Returns:
            pd.DataFrame: The data from the table.
        """
        if self.engine is None:
            self.init_db_engine()

        if self.engine:
            try:
                df = pd.read_sql_table(table_name, self.engine)
                return df
            except Exception as e:
                logger.error(f"Error reading table {table_name}: {e}")
                return pd.DataFrame()
        else:
            logger.error("Engine not initialised. Cannot read table.")
            return pd.DataFrame()

    def upload_to_db(self, df, table_name, if_exists='replace'):
    
        if self.engine is None:
            self.init_db_engine()
        
        if self.engine:
            try:
                df.to_sql(table_name, self.engine, if_exists=if_exists, index=False, method='multi')
                logger.info(f"Data successfully uploaded to {table_name}")
            except Exception as e:
                logger.error(f"Error uploading to database: {e}")
        else:
            logger.error("Database engine is not initialised. Please check your credentials.")

if __name__ == "__main__":
    # Connects to a PostgreSQL database using credentials from a YAML file,
    # lists all tables in the database (raw), and prints them.
    connector = DatabaseConnector("db_creds_raw.yaml")
    engine = connector.init_db_engine()
    tables = connector.list_db_tables()

    if engine and tables:
        logger.info("Connected to the database!")
        logger.info(f"Tables in DB: {tables}")
    else:
        logger.error("Could not connect to the database.")
