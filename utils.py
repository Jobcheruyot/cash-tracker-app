from datetime import datetime
import streamlit as st

def today():
    return datetime.now().date()

def load_form_fields(existing):
    data = {}
    st.markdown("### 🧾 Sales and Cash Summary")
    data["Expected Cash"] = st.number_input("Expected Cash", value=existing.get("Expected Cash", 0.0))
    data["Cash Pickups"] = st.number_input("Cash Pickups", value=existing.get("Cash Pickups", 0.0))
    data["Variance"] = data["Expected Cash"] - data["Cash Pickups"]

    st.markdown("### 💳 Mobile Money Section")
    dropdown_options = ["Utilized", "Reversed", "Add Comment"]
    for method in ["Mpesa", "Vooma", "PDQ", "WHT", "Deposit"]:
        data[method] = st.selectbox(method, dropdown_options, index=0)

    st.markdown("### 🧮 Manual Adjustments")
    data["Manual Adjustment"] = st.number_input("Manual Adjustment", value=existing.get("Manual Adjustment", 0.0))
    return data

def compute_all_fields(data):
    return data