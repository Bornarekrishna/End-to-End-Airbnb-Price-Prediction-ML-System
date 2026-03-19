import os
import pandas as pd


class DataValidation:
    def __init__(self):
        self.data_path = os.path.join("artifacts", "raw_data", "Airbnb_data.csv")
        self.required_columns = [
            "id",
            "log_price",
            "property_type",
            "room_type",
            "amenities",
            "accommodates",
            "bathrooms",
            "bed_type",
            "cancellation_policy",
            "cleaning_fee",
            "city",
            "description",
            "first_review",
            "host_has_profile_pic",
            "host_identity_verified",
            "host_response_rate",
            "host_since",
            "instant_bookable",
            "last_review",
            "latitude",
            "longitude",
            "name",
            "neighbourhood",
            "number_of_reviews",
            "review_scores_rating",
            "thumbnail_url",
            "zipcode",
            "bedrooms",
            "beds"
        ]

    def validate_data(self):
        print("Starting data validation...")

        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at: {self.data_path}")

        df = pd.read_csv(self.data_path)

        if df.empty:
            raise ValueError("Dataset is empty.")

        missing_columns = [col for col in self.required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        print("All required columns are present.")
        print(f"Dataset shape: {df.shape}")
        print("Data validation completed successfully.")

        return True


if __name__ == "__main__":
    validator = DataValidation()
    validator.validate_data()