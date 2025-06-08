import streamlit as st
from datetime import date
import io
from weather import get_weather
from itinerary import generate_llm_itinerary
from database import save_itinerary, get_user_itineraries

# Ensure user is logged in
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("🔐 Please log in first.")
    st.stop()

# ----- Tab 1: Itinerary Generator -----
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
                ["Culture", "Nature", "Food", "Museums", "Nightlife", "Shopping"],
                default=["Food", "Culture"]
            )
            currency = st.selectbox("Choose your Currency:", ["USD", "INR", "EURO"])

        budget = st.slider("Select your budget", min_value=500, max_value=200000, step=500, value=10000)
        submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        weather = get_weather(location)
        st.success(f"📍 **{location}** | Weather: {weather}")
        itinerary = generate_llm_itinerary(location, days, interests, weather, people, currency, budget)

        for day_text in itinerary.split("\n\n"):
            st.markdown(f"<div class='card'>{day_text}</div>", unsafe_allow_html=True)

        save_itinerary(
            st.session_state.username, location, str(start_date), days,
            interests, people, currency, budget, weather, itinerary
        )

        report_bytes = io.BytesIO(itinerary.encode("utf-8"))
        st.download_button(
            "📄 Download This Itinerary",
            report_bytes,
            file_name=f"{location}_itinerary.txt",
            mime="text/plain"
        )

# ----- Tab 2: Saved Trips -----
def saved_trips_tab():
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

# ----- Tab 3: User Profile -----

    st.title("👤 User Profile")
    st.markdown(f"### 👋 Welcome, **{st.session_state.username}**!")
    st.markdown("This is your profile page. You can enhance this to include user preferences, history, etc.")

# ----- Tab 4: Logout -----
def logout_tab():
    st.title("🚪 Logout")
    st.success("You are now logged out. Please close the app or go to the login page.")
    if st.button("🔄 Logout Now"):
        st.session_state.clear()
        st.rerun()

# ----- Tabs UI -----
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Itinerary", "💾 Saved Trips", "👤 Profile", "🚪 Logout"])

with tab1:
    itinerary_tab()
with tab2:
    saved_trips_tab()
with tab3:
    profile_tab()
with tab4:
    logout_tab()
