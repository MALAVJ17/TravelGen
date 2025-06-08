import streamlit as st
import random
import string
from user_db import create_users_table, add_user, check_user1, check_user, reset_password
import yagmail

# Ensure users table exists
create_users_table()

def auth_ui():
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Signup", "🔑 Forgot Password"])

    # ---- LOGIN TAB ----
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if check_user1(username, password):
                st.success("Login successful!")
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Invalid credentials.")

    # ---- SIGNUP TAB ----
    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            if add_user(new_user, new_pass):
                st.success("Signup successful! You can now log in.")
            else:
                st.warning("Username already exists.")

    # ---- FORGOT PASSWORD TAB ----
    with tab3:
        step = st.session_state.get("reset_step", 1)

        if step == 1:
            username = st.text_input("Enter your registered username")
            if st.button("Proceed"):
                # Check if the username exists
                if check_user(username, None, only_check=True):  # Modify check_user to support this
                    st.session_state.reset_username = username
                    st.session_state.reset_step = 2
                else:
                    st.error("Username not found.")
        elif step == 2:
            new_pass = st.text_input("Enter new password", type="password")
            confirm_pass = st.text_input("Confirm new password", type="password")
            if st.button("Reset Password"):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    reset_password(st.session_state.reset_username, new_pass)
                    st.success("Password reset successful. You can now log in.")
                    # Reset session state
                    st.session_state.reset_step = 1
                    st.session_state.reset_username = None
