import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict import PredictPipeline

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Airbnb Price Prediction", page_icon="🏠", layout="wide")

# ===== AIRBNB PREMIUM CSS =====
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.main-title {
    text-align: center;
    font-size: 40px;
    color: #FF5A5F;
    font-weight: bold;
}
.sub-text {
    text-align: center;
    color: #ccc;
}
.card {
    background-color: #1c1f26;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #2a2a2a;
}
.stButton>button {
    background-color: #FF5A5F;
    color: white;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
    width: 100%;
}
.stButton>button:hover {
    background-color: #ff3b3f;
}
</style>
""", unsafe_allow_html=True)

# ===================== TITLE =====================
st.markdown("""
<h1 style='text-align: center; color: #FF5A5F;'>
🏠 Airbnb Price Prediction
</h1>
<p style='text-align: center; color: white;'>
Smart pricing for your perfect stay 💡
</p>
""", unsafe_allow_html=True)

# Load pipeline
pipeline = PredictPipeline()

# ===================== FORM =====================
with st.form("prediction_form"):

    st.subheader("🏡 Property Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox("City", ["Boston", "Chicago", "DC", "LA", "NYC", "SF"])
        property_type = st.selectbox(
            "Property Type",
            ["Apartment", "House", "Condominium", "Townhouse", "Loft",
             "Guesthouse", "Bed & Breakfast", "Bungalow", "Villa", "Dorm", "Other"]
        )
        room_type = st.selectbox("Room Type", ["Entire home/apt", "Private room", "Shared room"])
        bed_type = st.selectbox("Bed Type", ["Airbed", "Couch", "Futon", "Pull-out Sofa", "Real Bed"])

    with col2:
        cancellation_policy = st.selectbox(
            "Cancellation Policy",
            ["Flexible","Moderate","Strict","Super Strict 30","Super Strict 60"]
        )
        accommodates = st.number_input("Accommodates", min_value=1, step=1)
        bathrooms = st.number_input("Bathrooms", min_value=0, step=1)
        bedrooms = st.number_input("Bedrooms", min_value=0, step=1)

    with col3:
        beds = st.number_input("Beds", min_value=0, step=1)
        amenities_count = st.number_input("Amenities Count", min_value=0, step=1)
        number_of_nights = st.number_input("Number of Nights", min_value=1, step=1)
        cleaning_fee = st.selectbox("Cleaning Fee", ["No", "Yes"])
        cleaning_fee = 1 if cleaning_fee == "Yes" else 0

    st.subheader("👤 Host & Review Details")

    col4, col5, col6 = st.columns(3)

    with col4:
        instant_bookable = st.selectbox("Instant Bookable", ["No", "Yes"])
        instant_bookable = 1 if instant_bookable == "Yes" else 0

        host_has_profile_pic = st.selectbox("Host Has Profile Pic", ["No", "Yes"])
        host_has_profile_pic = 1 if host_has_profile_pic == "Yes" else 0

        host_identity_verified = st.selectbox("Host Identity Verified", ["No", "Yes"])
        host_identity_verified = 1 if host_identity_verified == "Yes" else 0

    with col5:
        host_response_rate = st.number_input("Host Response Rate (%)", min_value=0.0, max_value=100.0, step=1.0)
        host_years = st.number_input("Host Experience (Years)", min_value=0, step=1)
        number_of_reviews = st.number_input("Number of Reviews", min_value=0, step=1)

    with col6:
        review_scores_rating = st.number_input("Review Score Rating", min_value=0.0, max_value=100.0, step=1.0)
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")

    cancel_map = {
        "Flexible":"flexible",
        "Moderate":"moderate",
        "Strict":"strict",
        "Super Strict 30":"super_strict_30",
        "Super Strict 60":"super_strict_60"
    }

    input_data = {
        "property_type": property_type,
        "room_type": room_type,
        "bed_type": bed_type,
        "cancellation_policy": cancel_map[cancellation_policy],
        "cleaning_fee": cleaning_fee,
        "city": city,
        "accommodates": accommodates,
        "bathrooms": bathrooms,
        "host_has_profile_pic": host_has_profile_pic,
        "host_identity_verified": host_identity_verified,
        "host_response_rate": host_response_rate,
        "instant_bookable": instant_bookable,
        "latitude": latitude,
        "longitude": longitude,
        "number_of_reviews": number_of_reviews,
        "review_scores_rating": review_scores_rating,
        "bedrooms": bedrooms,
        "beds": beds,
        "amenities_count": amenities_count,
        "host_years": host_years
    }

    submit_button = st.form_submit_button("🚀 Predict Price")

    # ===== STORE DATA =====
if submit_button:
    st.session_state["input_data"] = input_data
    st.session_state["nights"] = number_of_nights
    st.switch_page("pages/2_Result.py")

st.markdown("</div>", unsafe_allow_html=True)

