import streamlit as st
from core.itinerary_tab import itinerary_tab
from core.saved_trips_tab import saved_trips_tab
from core.profile_tab import profile_tab

# Ensure user is logged in
if not st.session_state.get("authenticated"):
    st.error("Please log in first.")
    st.stop()

# Set default tab
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Generate Itinerary"

# Top Nav Buttons
st.markdown("### ✈️ Travel Itinerary Generator")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("🗺 Generate Itinerary"):
        st.session_state.active_tab = "Generate Itinerary"
with col2:
    if st.button("💾 My Saved Trips"):
        st.session_state.active_tab = "My Saved Trips"
with col3:
    if st.button("👤 My Profile"):
        st.session_state.active_tab = "My Profile"
with col4:
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.rerun()

st.write("---")

# Render active tab
if st.session_state.active_tab == "Generate Itinerary":
    itinerary_tab()
elif st.session_state.active_tab == "My Saved Trips":
    saved_trips_tab()
elif st.session_state.active_tab == "My Profile":
    profile_tab()
