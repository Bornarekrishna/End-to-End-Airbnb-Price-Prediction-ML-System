from src.user_form import user_form
from src.predict import PredictPipeline


if __name__ == "__main__":
    print("\nStarting Airbnb Price Prediction App...\n")

    # Collect user input from console
    input_data, number_of_nights = user_form()

    # Load prediction pipeline
    pipeline = PredictPipeline()

    # Get prediction result
    result = pipeline.predict_price(input_data, number_of_nights)

    print("\n" + "=" * 50)
    print("           Prediction Result")
    print("=" * 50)
    print(f"Predicted Nightly Price : {result['nightly_price']}")
    print(f"Number of Nights        : {result['number_of_nights']}")
    print(f"Total Stay Price        : {result['total_price']}")
    print("=" * 50)