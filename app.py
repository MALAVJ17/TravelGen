import streamlit as st
from auth import auth_ui
from database import init_db
from core.itinerary_tab import itinerary_tab
from core.saved_trips_tab import saved_trips_tab
from core.profile_tab import profile_tab


st.set_page_config(page_title="Travel Itinerary Generator", layout="wide")
init_db()

# --- Session State Setup ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Generate Itinerary"
if "username" not in st.session_state:
    st.session_state.username = ""

# --- AUTHENTICATION FLOW ---
if not st.session_state.authenticated:
    st.title("✈️ Travel Itinerary Generator - Login")
    auth_ui()  # Includes Login, Signup, Forgot Password
    st.stop()

# --- NAVIGATION HEADER ---
st.markdown("## ✈️ Travel Itinerary Generator")
nav1, nav2, nav3, nav4 = st.columns([1, 1, 1, 1])

with nav1:
    if st.button("🗺 Generate Itinerary"):
        st.session_state.active_tab = "Generate Itinerary"
with nav2:
    if st.button("💾 My Saved Trips"):
        st.session_state.active_tab = "My Saved Trips"
with nav3:
    if st.button("👤 My Profile"):
        st.session_state.active_tab = "My Profile"
with nav4:
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

st.write("---")

# --- MAIN CONTENT ---
if st.session_state.active_tab == "Generate Itinerary":
    itinerary_tab()
elif st.session_state.active_tab == "My Saved Trips":
    saved_trips_tab()
elif st.session_state.active_tab == "My Profile":
    profile_tab()
