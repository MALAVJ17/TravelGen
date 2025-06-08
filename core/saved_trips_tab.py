import streamlit as st
import io
from database import get_user_itineraries

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
            st.download_button(f"📄 Download {loc} Itinerary", download_bytes, file_name=f"{loc}_trip_{trip_id}.txt", mime="text/plain", key=f"dl_{i}")
