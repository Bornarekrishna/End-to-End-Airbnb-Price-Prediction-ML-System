import os
import joblib
import pandas as pd
import numpy as np


class PredictPipeline:
    def __init__(self):
        # Paths of saved model and transformation artifacts
        self.model_path = os.path.join("models", "best_model.pkl")
        self.encoders_path = os.path.join("artifacts", "transformed_data", "label_encoders.pkl")
        self.top_property_types_path = os.path.join("artifacts", "transformed_data", "top_10_property_types.pkl")
        self.model_columns_path = os.path.join("artifacts", "transformed_data", "model_columns.pkl")

        # Load trained model and required preprocessing artifacts
        self.model = joblib.load(self.model_path)
        self.encoders = joblib.load(self.encoders_path)
        self.top_10_property_types = joblib.load(self.top_property_types_path)
        self.model_columns = joblib.load(self.model_columns_path)

        print("Prediction pipeline loaded successfully.")
        print(f"Model loaded from: {self.model_path}")

    def preprocess_input(self, input_data: dict) -> pd.DataFrame:
        """
        Convert raw user input into model-ready format.
        This step must match the same transformation logic used during training.
        """
        print("\nStarting input preprocessing...")

        # Convert single input dictionary into DataFrame
        df = pd.DataFrame([input_data])

        # Handle rare property types
        if "property_type" in df.columns:
            if df.loc[0, "property_type"] not in self.top_10_property_types:
                df.loc[0, "property_type"] = "Other"

        # Apply one-hot encoding to property_type and city
        df = pd.get_dummies(df, columns=["property_type", "city"], drop_first=False,dtype=int)

        # Apply label encoding to categorical columns
        label_cols = ["room_type", "bed_type", "cancellation_policy"]
        for col in label_cols:
            if col in df.columns:
                le = self.encoders[col]
                df[col] = le.transform(df[col])

        # Reindex to match exact training columns
        df = df.reindex(columns=self.model_columns, fill_value=0)

        print("Input preprocessing completed successfully.")
        return df
    def predict_price(self, input_data: dict, number_of_nights: int) -> dict:
        """
        Predict nightly price and total stay price.
        """
        print("\nGenerating prediction...")

        # Transform user input into model-ready format
        processed_input = self.preprocess_input(input_data)

        # Predict log_price
        log_prediction = self.model.predict(processed_input)[0]

        # Convert log_price back to actual nightly price
        nightly_price = float(np.exp(log_prediction))

        # Calculate total price for user-entered nights
        total_price = nightly_price * number_of_nights

        # Create price range (±10%)
        lower_price = nightly_price * 0.9
        upper_price = nightly_price * 1.1


        print("Prediction generated successfully.")

        return {
        "nightly_price": round(nightly_price, 2),
        "lower_price": round(lower_price, 2),
        "upper_price": round(upper_price, 2),
        "number_of_nights": int(number_of_nights),
        "total_price": round(total_price, 2)}