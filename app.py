import streamlit as st
from auth_config import login_user
from gsheets_manager import submit_data, get_existing_entry, is_edit_allowed, update_data
from datetime import datetime

st.set_page_config(page_title="Cash Tracker App", layout="wide")

# --- Login ---
name, is_authenticated, username = login_user()
if not is_authenticated:
    st.stop()

st.title("🧾 Daily Cash Submission")

branches = ["BANDARI", "BURUBURU", "DONHOLM", "NAKURU", "KISUMU"]
action = st.radio("Choose Action", ["Submit New", "Edit Existing"])

with st.form("cash_form"):
    branch = st.selectbox("Select Branch", branches, index=None)
    date = st.date_input("Select Date")
    expected_cash = st.number_input("Expected Cash", min_value=0)
    mpesa = st.number_input("Mpesa", min_value=0)
    vooma = st.number_input("Vooma", min_value=0)
    pdq = st.number_input("PDQ", min_value=0)
    wht = st.number_input("WHT", min_value=0)
    deposit = st.number_input("Deposits", min_value=0)
    manual_adj = st.number_input("Manual Adjustment", min_value=0)
    submitted_by = name
    submitted_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    submitted = st.form_submit_button("Submit Entry")
    if submitted and branch:
        row = [
            branch,
            date.strftime("%Y-%m-%d"),
            submitted_on,
            submitted_by,
            expected_cash,
            "", "",  # Cash Pickups, Variance (optional)
            mpesa,
            vooma,
            pdq,
            wht,
            deposit,
            manual_adj,
        ]

        row_index, record = get_existing_entry(branch, date.strftime("%Y-%m-%d"))

        if action == "Submit New" and not record:
            submit_data(row)
            st.success("Entry submitted successfully.")
        elif action == "Edit Existing" and record:
            if is_edit_allowed(record["Timestamp"]):
                update_data(row_index, row)
                st.success("Entry updated successfully.")
            else:
                st.error("Editing window expired (7 days).")
        else:
            st.warning("No record found to edit or already exists.")
