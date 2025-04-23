import pandas as pd 
from data_cleaning import DataCleaning 
from data_extraction import DataExtraction
from data_utils import DataConnector 

db = DatabaseConnector()              # create dependency
extractor = DataExtractor(db)        # inject it
