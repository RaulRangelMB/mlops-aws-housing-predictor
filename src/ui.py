import streamlit as st
import requests

API_URL = "https://zk7qrgpllsqutxwtz7xqfjfnxm0nezko.lambda-url.eu-north-1.on.aws/"

# Page configuration
st.set_page_config(page_title="Housing Price Predictor", layout="centered")

st.title("🏠 Cloud-Native Housing Predictor")
st.markdown("This interface connects to a serverless AWS Lambda backend to predict housing prices in real-time via a Scikit-Learn regression model.")

st.divider()

# Create a clean layout with columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Neighborhood Details")
    med_inc = st.slider("Median Income (in $10k)", 0.0, 15.0, 8.32)
    house_age = st.slider("House Age (Years)", 1.0, 50.0, 41.0)
    ave_rooms = st.slider("Average Rooms", 1.0, 10.0, 6.98)
    ave_bedrms = st.slider("Average Bedrooms", 0.5, 5.0, 1.02)

with col2:
    st.subheader("Location & Scale")
    population = st.number_input("Population", 10.0, 10000.0, 322.0)
    ave_occup = st.slider("Average Occupancy", 1.0, 10.0, 2.55)
    latitude = st.number_input("Latitude", 32.0, 42.0, 37.88)
    longitude = st.number_input("Longitude", -125.0, -114.0, -122.23)

st.divider()

# trigger button
if st.button("Predict Housing Price", type="primary", use_container_width=True):
    payload = {
        "features": [med_inc, house_age, ave_rooms, ave_bedrms, population, ave_occup, latitude, longitude]
    }
    
    # Send the request with a loading spinner
    with st.spinner("Waiting for answer..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"**Estimated Value:** ${result['estimated_usd']:,.2f}")
                st.caption(f"Raw Model Output: {result['predicted_raw']}")
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to the cloud: {e}")