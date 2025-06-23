import streamlit as st
import streamlit_authenticator as stauth

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "admin123",
        },
        "ruaka": {
            "name": "Ruaka",
            "password": "ruaka123",
        },
        "buruburu": {
            "name": "Buruburu",
            "password": "buru123",
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cash_app",
    "abcdef",
    cookie_expiry_days=1
)

def login_user():
    name, auth_status, username = authenticator.login("Login", "main")
    if auth_status == False:
        st.error("Incorrect username or password.")
    elif auth_status == None:
        st.warning("Please enter your username and password.")
    elif auth_status:
        branch = username if username != "admin" else "admin"
        return {"authenticated": True, "username": username, "branch": branch}
    return {"authenticated": False}
