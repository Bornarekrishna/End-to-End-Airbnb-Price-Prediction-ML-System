import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataTransformation:
    def __init__(self):
        self.input_path = os.path.join("artifacts", "processed_data", "cleaned_airbnb_data.csv")
        self.output_dir = os.path.join("artifacts", "transformed_data")
        self.output_path = os.path.join(self.output_dir, "train_transformed.csv")

        # Artifact paths
        self.encoders_path = os.path.join(self.output_dir, "label_encoders.pkl")
        self.top_property_types_path = os.path.join(self.output_dir, "top_10_property_types.pkl")
        self.model_columns_path = os.path.join(self.output_dir, "model_columns.pkl")

    def transform_data(self):
        print("Starting data transformation...")

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        df = pd.read_csv(self.input_path)

        # Keep top 10 property types, rest -> Other
        top_10_property_types = df["property_type"].value_counts().nlargest(11).index.tolist()
        df["property_type"] = df["property_type"].apply(
            lambda x: x if x in top_10_property_types else "Other"
        )

        # One-hot encode property_type and city
        df = pd.get_dummies(df, columns=["property_type", "city"], drop_first=False, dtype=int)

        # Label encode selected columns
        label_cols = ["room_type", "bed_type", "cancellation_policy"]
        encoders = {}

        for col in label_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le

        os.makedirs(self.output_dir, exist_ok=True)

        # Save transformed training data
        df.to_csv(self.output_path, index=False)

        # Save transformation artifacts
        joblib.dump(encoders, self.encoders_path)
        joblib.dump(top_10_property_types, self.top_property_types_path)
        joblib.dump(df.drop("log_price", axis=1).columns.tolist(), self.model_columns_path)

        print("Data transformation completed successfully.")
        print(f"Transformed data saved at: {self.output_path}")
        print(f"Encoders saved at: {self.encoders_path}")
        print(f"Top property types saved at: {self.top_property_types_path}")
        print(f"Model columns saved at: {self.model_columns_path}")
        print(f"Final transformed shape: {df.shape}")

        return df


if __name__ == "__main__":
    transformer = DataTransformation()
    transformer.transform_data()