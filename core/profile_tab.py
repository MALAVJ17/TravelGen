import streamlit as st
import re
import datetime

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\+?\d{10,15}$", phone)

def profile_tab():
    st.title("👤 User Profile")

    default_values = {
        'name': st.session_state.get('username', 'Guest'),
        'gender': "Prefer not to say",
        'phone': "",
        'email': "",
        'interests': [],
        'dob': None,
        'location': "",
        'editing_profile': False
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.markdown(f"### 👋 Welcome, **{st.session_state.name}**!")

    st.markdown("""
        <style>
            .profile-box {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #444;
                margin-bottom: 20px;
                font-size: 16px;
                color: #f1f1f1;
            }
            .profile-label {
                font-weight: bold;
                color: #f5a623;
            }
            .profile-header {
                font-size: 22px;
                margin-bottom: 10px;
                font-weight: 600;
            }
            .edit-button {
                margin-top: 15px;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.editing_profile:
        with st.container():
            st.markdown('<div class="profile-box">', unsafe_allow_html=True)
            st.markdown('<div class="profile-header">📋 Profile Information</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<span class="profile-label">🧑 Name:</span> {st.session_state.name}', unsafe_allow_html=True)
                st.markdown(f'<span class="profile-label">⚧️ Gender:</span> {st.session_state.gender}', unsafe_allow_html=True)
                st.markdown(f'<span class="profile-label">📞 Phone:</span> {st.session_state.phone or "Not provided"}', unsafe_allow_html=True)
                st.markdown(f'<span class="profile-label">📧 Email:</span> {st.session_state.email or "Not provided"}', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<span class="profile-label">🎯 Interests:</span> {", ".join(st.session_state.interests) if st.session_state.interests else "None"}', unsafe_allow_html=True)
                st.markdown(f'<span class="profile-label">🗓️ Date of Birth:</span> {st.session_state.dob or "Not provided"}', unsafe_allow_html=True)
                st.markdown(f'<span class="profile-label">🌍 Location:</span> {st.session_state.location or "Not provided"}', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.button("✏️ Edit Profile", on_click=lambda: st.session_state.update({'editing_profile': True}), key="edit_btn")

    else:
        st.subheader("✏️ Edit Your Profile")

        new_name = st.text_input("Full Name", st.session_state.name)
        gender_options = ["Male", "Female", "Non-binary", "Prefer not to say"]
        new_gender = st.selectbox("Gender", gender_options, index=gender_options.index(st.session_state.gender))
        new_phone = st.text_input("Phone Number", st.session_state.phone)
        new_email = st.text_input("Email Address", st.session_state.email)
        interests_list = ["Travel", "Technology", "Music", "Sports", "Reading", "Movies", "Gaming", "Art", "Fitness", "Cooking"]
        new_interests = st.multiselect("Interests", interests_list, default=st.session_state.interests)
        new_dob = st.date_input("Date of Birth", value=st.session_state.dob or datetime.date(2000, 1, 1), max_value=datetime.date.today())
        new_location = st.text_input("Location (Country/City)", st.session_state.location)

        col1, col2 = st.columns(2)
        if col1.button("✅ Save"):
            if not new_name.strip():
                st.warning("Full Name is required.")
            elif new_email and not is_valid_email(new_email):
                st.warning("Please enter a valid email address.")
            elif new_phone and not is_valid_phone(new_phone):
                st.warning("Please enter a valid phone number (10–15 digits).")
            elif new_dob > datetime.date.today():
                st.warning("Date of Birth cannot be in the future.")
            else:
                st.session_state.name = new_name.strip()
                st.session_state.gender = new_gender
                st.session_state.phone = new_phone.strip()
                st.session_state.email = new_email.strip()
                st.session_state.interests = new_interests
                st.session_state.dob = str(new_dob)
                st.session_state.location = new_location.strip()
                st.session_state.editing_profile = False
                st.success("Profile updated successfully!")

        if col2.button("❌ Cancel"):
            st.session_state.editing_profile = False
