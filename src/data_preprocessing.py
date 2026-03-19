import os
import pandas as pd
import numpy as np


class DataPreprocessing:
    def __init__(self):
        self.input_path = os.path.join("artifacts", "raw_data", "Airbnb_Data.csv")
        self.output_dir = os.path.join("artifacts", "processed_data")
        self.output_path = os.path.join(self.output_dir, "cleaned_airbnb_data.csv")

    def preprocess_data(self):
        print("Starting data preprocessing...")

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        df = pd.read_csv(self.input_path)

        # Drop unnecessary columns
        columns_to_drop = ["id", "thumbnail_url", 'first_review', 'last_review', 'neighbourhood',"description", "name", "zipcode"]
        df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

        # Transform Columns in correct order
        # convert amenities into numbers of amenities
        df['amenities_count'] = df['amenities'].apply(lambda x: len(str(x).split(',')))

        # Use host experience instead of host since
        # Handle potential date parsing errors by coercing to NaT
        current_year = pd.Timestamp.now().year
        df["host_years"] = current_year - pd.to_datetime(df["host_since"], errors="coerce").dt.year

        # Ensure host_response_rate is string, replace '%', then convert to numeric, coercing errors
        df['host_response_rate'] = df['host_response_rate'].astype(str).str.replace('%', '')
        df['host_response_rate'] = pd.to_numeric(df['host_response_rate'], errors='coerce')

        # cleaning_fee is already boolean, direct conversion to int
        df['cleaning_fee'] = df['cleaning_fee'].astype(int)

        # instant_bookable needs mapping from 't'/'f' to 1/0
        df['instant_bookable'] = df['instant_bookable'].map({'t': 1, 'f': 0}).astype(int)

        # Fill numeric missing values
        numeric_fill_cols = ["bathrooms", "bedrooms", "beds", "review_scores_rating"]
        for col in numeric_fill_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

        # Fill categorical missing values
        categorical_fill_cols = ["host_has_profile_pic","host_identity_verified"]
        for col in categorical_fill_cols:
            if col in df.columns:
                df[col] = df[col].fillna("f")

        # host_has_profile_pic and host_identity_verified needs mapping from 't'/'f' to 1/0
        mapping_col = ['host_has_profile_pic', 'host_identity_verified']
        for col in mapping_col:
            if col in df.columns:
                df[col] = df[col].map({'t': 1, 'f': 0}).astype(int)

        # Fill Host Response Rate and Host years by Median
        host_col = ["host_response_rate","host_years"]
        for col in host_col:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

        # Drop original columns after transformation
        df.drop(columns=["amenities", "host_since"], inplace=True, errors="ignore")

        # Save processed file
        os.makedirs(self.output_dir, exist_ok=True)
        df.to_csv(self.output_path, index=False)

        print("Data preprocessing completed successfully.")
        print(f"Processed data saved at: {self.output_path}")
        print(f"Final shape: {df.shape}")

        return df


if __name__ == "__main__":
    preprocessor = DataPreprocessing()
    preprocessor.preprocess_data()