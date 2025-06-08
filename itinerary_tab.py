import streamlit as st
from datetime import date
import io
from weather import get_weather
from itinerary import generate_llm_itinerary
from database import save_itinerary

def itinerary_tab():
    st.title("🏖️ AI Itinerary Generator")


    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 Destination", "Tokyo")
            start_date = st.date_input("📅 Start Date", date.today())
            people = st.number_input("People", min_value=1, max_value=10, value=2)
        with col2:
            days = st.number_input("📆 Duration (Days)", min_value=1, max_value=15, value=3)
            interests = st.multiselect(
    "🎯 Interests",
    [
        "Culture", "Nature", "Food", "Museums", "Nightlife", "Shopping",
        "Adventure", "Beaches", "Hiking", "Photography", "Wildlife",
        "Temples", "Festivals", "History", "Art", "Architecture",
        "Relaxation", "Mountains", "Camping", "Diving", "Skiing",
        "Roadtrips", "Cruise", "Markets", "Theatre", "Yoga",
        "Spa", "Music", "Local", "Heritage"
    ],
    default=["Food", "Culture"]
)

            currency = st.selectbox("Choose your Currency:", ["USD", "INR", "EURO"])

        budget = st.slider("Select your budget", min_value=500, max_value=200000, step=500, value=10000)

        submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        # Fetch weather info
        weather = get_weather(location)
        st.success(f"📍 **{location}** | Weather: {weather}")

        # Generate itinerary from LLM
        itinerary = generate_llm_itinerary(location, days, interests, weather, people, currency, budget)

        # Display itinerary day by day inside styled cards
        for day_text in itinerary.split("\n\n"):
            st.markdown(f"<div class='card'>{day_text}</div>", unsafe_allow_html=True)

        # Save itinerary in DB
        save_itinerary(
            st.session_state.username, location, str(start_date), days,
            interests, people, currency, budget, weather, itinerary
        )

        # Prepare downloadable text file
        report_bytes = io.BytesIO(itinerary.encode("utf-8"))
        st.download_button(
            "📄 Download This Itinerary",
            report_bytes,
            file_name=f"{location}_itinerary.txt",
            mime="text/plain"
        )
