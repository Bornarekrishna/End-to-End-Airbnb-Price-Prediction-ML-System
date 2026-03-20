import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


class ModelTraining:
    def __init__(self):
        # Path of transformed dataset created in previous stage
        self.input_path = os.path.join("artifacts", "transformed_data", "train_transformed.csv")

        # Directory where trained model will be saved
        self.model_dir = "models"

        # Final best model file path
        self.model_path = os.path.join(self.model_dir, "best_model.pkl")

    def evaluate_model(self, y_true, y_pred):
        """
        Calculate evaluation metrics for regression models.
        Returns:
            r2   : R² Score
            mae  : Mean Absolute Error
            rmse : Root Mean Squared Error
        """
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return r2, mae, rmse

    def train_models(self):
        print("=" * 60)
        print("Starting Model Training Stage")
        print("=" * 60)

        # Check if transformed dataset exists
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        print(f"Loading transformed dataset from: {self.input_path}")
        df = pd.read_csv(self.input_path)

        print(f"Dataset loaded successfully with shape: {df.shape}")

        # Separate features and target variable
        X = df.drop("log_price", axis=1)
        y = df["log_price"]

        print(f"Feature matrix shape: {X.shape}")
        print(f"Target vector shape: {y.shape}")

        # Split data into training and testing sets
        print("\nSplitting dataset into train and test sets...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"Training set shape: X_train={X_train.shape}, y_train={y_train.shape}")
        print(f"Testing set shape : X_test={X_test.shape}, y_test={y_test.shape}")

        # Define models to compare
        models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(random_state=42),
            "Random Forest": RandomForestRegressor(
                n_estimators=400,
                max_depth=30,
                min_samples_split=5,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=42
            ),
            "XGBoost": XGBRegressor(
                n_estimators=800,
                learning_rate=0.03,
                max_depth=10,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        }

        best_model = None
        best_model_name = None
        best_r2 = -np.inf

        print("\nTraining and evaluating multiple models...")

        # Train each model and compare performance
        for name, model in models.items():
            print("\n" + "-" * 60)
            print(f"Training model: {name}")
            print("-" * 60)

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            r2, mae, rmse = self.evaluate_model(y_test, y_pred)

            print(f"{name} Performance:")
            print(f"R2 Score : {r2*100:.4f}")
            print(f"MAE      : {mae:.4f}")
            print(f"RMSE     : {rmse:.4f}")

            # Select the model with highest R² score
            if r2 > best_r2:
                best_r2 = r2
                best_model = model
                best_model_name = name

        # Save best model
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(best_model, self.model_path)

        print("\n" + "=" * 60)
        print("Model Training Completed Successfully")
        print("=" * 60)
        print(f"Best model selected : {best_model_name}")
        print(f"Best R2 Score       : {best_r2:.4f}")
        print(f"Best model saved at : {self.model_path}")


if __name__ == "__main__":
    trainer = ModelTraining()
    trainer.train_models()