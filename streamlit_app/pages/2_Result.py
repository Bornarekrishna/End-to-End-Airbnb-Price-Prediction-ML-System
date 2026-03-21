import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.predict import PredictPipeline

st.set_page_config(page_title="Prediction Result", layout="wide")

pipeline = PredictPipeline()

st.title("🎉 Your Price Prediction")

if "input_data" not in st.session_state:
    st.warning("No data found. Please go back.")
    st.stop()

data = st.session_state["input_data"]
nights = st.session_state["nights"]

result = pipeline.predict_price(data, nights)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric("💰 Nightly Price", f"${result['nightly_price']}")

with col2:
    st.metric("🧾 Total Price", f"${result['total_price']}")

st.info(f"📅 For {result['number_of_nights']} nights")

st.success("🙏 Thank you for using our Airbnb Price Prediction App!")

st.warning("""
⚠️ **Disclaimer:**  
    This prediction is based on a machine learning model with ~72% accuracy.  
    Prices may vary in real-world scenarios.  
    Please do not consider this as final pricing.
    """)

if st.button("⬅️ Back"):
    st.switch_page("app.py")