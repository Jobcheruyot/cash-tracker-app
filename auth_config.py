import streamlit as st
import streamlit_authenticator as stauth

def login_user():
    names = ['Admin']
    usernames = ['admin']
    passwords = ['admin123']
    hashed = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(
        names, usernames, hashed, 'cashtracker', 'abcdef', cookie_expiry_days=1
    )
    name, auth_status, username = authenticator.login('Login', 'main')
    if auth_status is False:
        st.error("Wrong username or password")
    elif auth_status is None:
        st.warning("Enter login credentials")
    return name, auth_status, username
