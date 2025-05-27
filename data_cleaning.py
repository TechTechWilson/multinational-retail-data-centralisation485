import pandas as pd
import numpy as np
import re

class DataCleaning:
    def clean_user_data(self, df):
        # Replace "NULL" strings with NaN
        df.replace("NULL", np.nan, inplace=True)
        
        # Convert date columns to datetime
        if 'date_of_birth' in df.columns:
            df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        if 'join_date' in df.columns:
            df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
        
        # Remove rows with NULL values
        df.dropna(inplace=True)
        
        # Convert user_id to string
        if 'user_id' in df.columns:
            df['user_id'] = df['user_id'].astype(str)
        
        return df

    def clean_card_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the card data according to requirements:
        - Changes "NULL" strings to NULL data type
        - Removes NULL values
        - Removes duplicate card numbers
        - Removes non-numerical card numbers
        - Converts "date_payment_confirmed" to datetime
        
        Args:
            df (pd.DataFrame): DataFrame containing card data
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Replace "NULL" strings with NaN
        df.replace("NULL", np.nan, inplace=True)
        
        # Convert date_payment_confirmed to datetime
        if 'date_payment_confirmed' in df.columns:
            df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce')
        
        # Remove non-numerical card numbers
        if 'card_number' in df.columns:
            df['card_number'] = df['card_number'].astype(str)
            df = df[df['card_number'].str.isnumeric()]
        
        # Remove duplicates based on card_number
        if 'card_number' in df.columns:
            df.drop_duplicates(subset=['card_number'], inplace=True)
        
        # Remove rows with NULL values
        df.dropna(inplace=True)
        
        return df

    def clean_store_data(self, df):
        df.replace("NULL", np.nan, inplace=True)
        df.dropna(inplace=True)

        if "opening_date" in df.columns:
            df["opening_date"] = pd.to_datetime(df["opening_date"], errors="coerce")
        df.dropna(subset=["opening_date"], inplace=True)

        if "staff_numbers" in df.columns:
            df["staff_numbers"] = df["staff_numbers"].astype(str).apply(lambda x: re.sub(r"\D", "", x))

        return df
    
    def _convert_weight(self, weight) -> float:
        """
        Converts a single weight value to kilograms.
        
        Args:
            weight: The weight value to convert (can be string or float)
            
        Returns:
            float: The weight in kilograms, or None if conversion fails
        """
        if pd.isna(weight):
            return None

        weight_str = str(weight).lower().strip()

        if 'kg' in weight_str:
            return float(weight_str.replace('kg', '').strip())
        if 'g' in weight_str:
            return float(weight_str.replace('g', '').strip()) / 1000
        if 'ml' in weight_str:
            return float(weight_str.replace('ml', '').strip()) / 1000
        if 'oz' in weight_str:
            return float(weight_str.replace('oz', '').strip()) * 0.0283495

        numeric = ''.join([c for c in weight_str if c.isdigit() or c == '.'])
        try:
            return float(numeric) / 1000
        except ValueError:
            return None

    def convert_product_weights(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts various weight formats to float kg.
        Assumes 1ml = 1g for simplicity.
        
        Args:
            df (pd.DataFrame): DataFrame containing product data with a 'weight' column
            
        Returns:
            pd.DataFrame: DataFrame with converted weights in kg
        """
        df['weight'] = df['weight'].apply(self._convert_weight)
        return df

    def clean_products_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the products data according to requirements:
        - Changes "NULL" strings to NULL data type
        - Removes NULL values
        - Converts all weights to kg units
        
        Args:
            df (pd.DataFrame): DataFrame containing product data
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Replace "NULL" strings with NaN
        df.replace("NULL", np.nan, inplace=True)
        
        # Convert weights to kg
        df = self.convert_product_weights(df)
        
        # Remove rows with NULL values
        df.dropna(inplace=True)
        
        return df

    def clean_orders_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the orders data according to requirements:
        - Removes unwanted columns (first_name, last_name, 1)
        
        Args:
            df (pd.DataFrame): DataFrame containing orders data
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Remove unwanted columns
        columns_to_remove = ['first_name', 'last_name', '1']
        df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
        
        return df

    def clean_date_times_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the date times data according to requirements:
        - Changes "NULL" strings to NULL data type
        - Removes NULL values
        - Converts "day", "month", and "year" columns to numeric values
        
        Args:
            df (pd.DataFrame): DataFrame containing date times data
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Replace "NULL" strings with NaN
        df.replace("NULL", np.nan, inplace=True)
        
        # Convert date columns to numeric
        date_columns = ['day', 'month', 'year']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with NULL values
        df.dropna(inplace=True)
        
        return df

