import streamlit as st
from auth import auth_ui
from weather import get_weather
from itinerary import generate_llm_itinerary
from datetime import date
import io
from database import init_db
from database import save_itinerary,get_user_itineraries
init_db()


st.set_page_config(page_title="Travel Itinerary Generator", layout="wide")

# Authenticate User
logged_in = auth_ui()
if not logged_in:
    st.stop()

page = st.sidebar.radio("📂 Menu", ["Generate Itinerary", "My Saved Trips"])


if page == "Generate Itinerary":
    st.title("🌍 AI-Powered Travel Itinerary Generator")
    st.markdown(f"👋 Welcome, **{st.session_state.username}**!")

    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("📍 Destination", "Tokyo")
            start_date = st.date_input("📅 Start Date", date.today())
            people = st.number_input("People", min_value=1, max_value=10, value=2)
        with col2:
            days = st.number_input("📆 Duration (Days)", min_value=1, max_value=15, value=3)
            interests = st.multiselect("🎯 Interests", ["Culture", "Nature", "Food", "Museums", "Nightlife", "Shopping"], default=["Food", "Culture"])
            currency = st.selectbox("Choose your Currency:", ["USD", "INR", "EURO"])

        budget = st.slider("Select your budget", min_value=500, max_value=200000, step=500, value=10000)

        submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        weather = get_weather(location)
        st.success(f"📍 **{location}** | Weather: {weather}")

        st.subheader("🧠 Generated Itinerary")
        itinerary = generate_llm_itinerary(location, days, interests, weather, people, currency, budget)

        for day_text in itinerary.split("\n\n"):
            st.markdown(f"<div class='card'>{day_text}</div>", unsafe_allow_html=True)

        save_itinerary(
            st.session_state.username,
            location,
            str(start_date),
            days,
            interests,
            people,
            currency,
            budget,
            weather,
            itinerary
        )

        report_bytes = io.BytesIO(itinerary.encode("utf-8"))
        st.download_button("📄 Download This Itinerary", report_bytes, file_name=f"{location}_itinerary.txt", mime="text/plain")
elif page == "My Saved Trips":
    st.title("📁 My Saved Itineraries")

    trips = get_user_itineraries(st.session_state.username)
    if not trips:
        st.info("No saved itineraries yet. Go generate one!")
    else:
        for i, trip in enumerate(trips):
            trip_id, loc, start, days, interests, people, curr, bud, weath, content = trip

            st.markdown(f"### ✈️ {loc} ({start})")
            st.markdown(f"**Duration:** {days} days | **Budget:** {curr} {bud} | **Weather:** {weath}")
            with st.expander("📋 View Itinerary"):
                st.markdown(content, unsafe_allow_html=True)

            download_bytes = io.BytesIO(content.encode("utf-8"))
            st.download_button(
                f"📄 Download {loc} Itinerary",
                download_bytes,
                file_name=f"{loc}_trip_{trip_id}.txt",
                mime="text/plain",
                key=f"dl_{i}"
            )
