import pandas as pd
import numpy as np
import re

class DataCleaning:
    def clean_user_data(self, df):
        df = df.dropna()

        if 'date_of_birth' in df.columns:
            df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        if 'join_date' in df.columns:
            df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
        df = df.dropna(subset=['date_of_birth', 'join_date'])

        if 'user_id' in df.columns:
            df['user_id'] = df['user_id'].astype(str)

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
    
    def convert_product_weights(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts various weight formats to float kg.
        Assumes 1ml = 1g for simplicity.
        """
    def convert_to_kg(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts various weight formats to float kg.
        Assumes 1ml = 1g for simplicity.
        """
        def _convert_weight(weight):
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

        df['weight'] = df['weight'].apply(_convert_weight)
        return df

