# Mappings used for label-encoded categorical columns
room_type_map = {
    "Entire home/apt": "Entire home/apt",
    "Private room": "Private room",
    "Shared room": "Shared room"
}

bed_type_map = {
    "Airbed": "Airbed",
    "Couch": "Couch",
    "Futon": "Futon",
    "Pull-out Sofa": "Pull-out Sofa",
    "Real Bed": "Real Bed"
}

cancellation_map = {
    "Flexible": "flexible",
    "Moderate": "moderate",
    "Strict": "strict",
    "Super_strict_30": "super_strict_30",
    "Super_strict_60": "super_strict_60"
}


def user_form():
    """
    Take user input from console and prepare it for prediction.
    Returns:
        data      -> dictionary of model input features
        no_nights -> number of nights entered by user
    """
    print("\n" + "=" * 50)
    print("        Airbnb Price Prediction Form")
    print("=" * 50 + "\n")

    data = {}

    # City input
    print("Available Cities: NYC, LA, SF, Chicago, DC, Boston")
    city = input("Enter City: ").strip()
    data["city"] = city

    # Property type input
    print("\nAvailable Property Types:")
    print("Apartment, House, Condominium, Townhouse, Loft, Guesthouse, Bed & Breakfast, Bungalow, Villa, Dorm, Other")
    prop = input("Enter Property Type: ").strip()
    data["property_type"] = prop

    # Room type input
    print("\nAvailable Room Types: Entire home/apt, Private room, Shared room")
    room = input("Enter Room Type: ").strip()
    data["room_type"] = room_type_map[room]

    # Accommodation details
    data["accommodates"] = int(input("\nNumber of guests accommodated: "))
    data["bedrooms"] = int(input("\nNumber of bedrooms: "))
    data["beds"] = int(input("\nNumber of beds: "))

    # Bed type input
    print("\nAvailable Bed Types: Airbed, Couch, Futon, Pull-out Sofa, Real Bed")
    bed = input("Enter Bed Type: ").strip().capitalize()
    data["bed_type"] = bed_type_map[bed]

    # Bathroom count
    data["bathrooms"] = float(input("\nNumber of bathrooms: "))

    # Number of nights for total stay calculation
    no_nights = int(input("How many nights do you want to stay? "))

    # Amenities and booking details
    data["amenities_count"] = int(input("\nNumber of amenities: "))
    data["cleaning_fee"] = int(input("Cleaning fee? (1 = Yes, 0 = No): "))
    data["instant_bookable"] = int(input("Instant bookable? (1 = Yes, 0 = No): "))

    # Host-related information
    data["host_response_rate"] = float(input("\nHost response rate (%): "))
    data["host_years"] = float(input("\nHost experience (years): "))
    data["host_identity_verified"] = int(input("\nHost identity verified? (1 = Yes, 0 = No): "))
    data["host_has_profile_pic"] = int(input("\nHost has profile pic? (1 = Yes, 0 = No): "))

    # Cancellation policy input
    print("\nAvailable Cancellation Policies: Flexible, Moderate, Strict, Super_strict_30, Super_strict_60")
    cancel = input("Enter Cancellation Policy: ").strip().capitalize()
    data["cancellation_policy"] = cancellation_map[cancel]

    # Exact property location
    data["latitude"] = float(input("\nLatitude: "))
    data["longitude"] = float(input("Longitude: "))

    # Review details
    data["number_of_reviews"] = int(input("\nMinimum Number of reviews: "))
    data["review_scores_rating"] = float(input("\nMinimum Review score rating: "))

    print("\nUser input collected successfully.")
    return data, no_nights