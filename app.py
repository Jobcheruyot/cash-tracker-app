import streamlit as st
from auth_config import login_user
from gsheets_manager import submit_data, get_existing_entry, is_edit_allowed, update_data
from utils import compute_all_fields, today, load_form_fields

# Page Setup
st.set_page_config(page_title="Cash Tracker", layout="wide")

# Auth
user_info = login_user()
if not user_info["authenticated"]:
    st.stop()

st.title("🧾 Daily Cash Tracking - {}".format(user_info["branch"].title()))

branch = user_info["branch"]
username = user_info["username"]

# Date Selection
selected_date = st.date_input("Select Date", value=today())

# Fetch existing entry if any
existing_data = get_existing_entry(branch, selected_date)
is_editing = existing_data is not None
can_edit = is_editing and is_edit_allowed(existing_data["timestamp"])

if is_editing and not can_edit:
    st.warning("You already submitted for this day and it's locked from editing after 7 days.")
    st.json(existing_data)
    st.stop()

# Form UI
form = st.form("entry_form")
with form:
    input_data = load_form_fields(existing_data or {})
    submitted = st.form_submit_button("Update Entry" if is_editing else "Submit Entry")

if submitted:
    final_data = compute_all_fields(input_data)
    if is_editing:
        update_data(branch, selected_date, final_data, username)
        st.success("Entry updated successfully.")
    else:
        submit_data(branch, selected_date, final_data, username)
        st.success("Entry submitted successfully.")