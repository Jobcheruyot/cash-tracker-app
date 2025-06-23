import streamlit as st
import streamlit_authenticator as stauth

names = ['Admin', 'Ruaka', 'Buruburu']
usernames = ['admin', 'ruaka', 'buruburu']
passwords = ['admin123', 'ruaka123', 'buru123']
roles = ['admin', 'user', 'user']

# 🔁 Corrected Hasher usage
hasher = stauth.Hasher()
hashed_passwords = hasher.generate(passwords)

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'cash_app',
    'abcdef',
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
