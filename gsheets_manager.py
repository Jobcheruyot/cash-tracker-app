import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import streamlit as st

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["GCP_SERVICE_ACCOUNT"], scope
)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1E9x7o_xsU67NYff2UNRtX9bwZpb9yfL2y52WofVF7f0")
entries_ws = sheet.worksheet("Daily_Entries")
logs_ws = sheet.worksheet("User_Logs")

def today():
    return datetime.now().date()

def get_existing_entry(branch, date):
    records = entries_ws.get_all_records()
    for r in records:
        if r["Branch"] == branch and r["Date"] == str(date):
            return r
    return None

def is_edit_allowed(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return (datetime.now() - dt).days <= 7

def submit_data(branch, date, data, user):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [branch, str(date), now, user] + list(data.values())
    entries_ws.append_row(row)
    logs_ws.append_row([now, branch, str(date), user, "NEW"])

def update_data(branch, date, data, user):
    records = entries_ws.get_all_records()
    for i, r in enumerate(records):
        if r["Branch"] == branch and r["Date"] == str(date):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [branch, str(date), now, user] + list(data.values())
            entries_ws.update(f"A{i+2}", [row])
            logs_ws.append_row([now, branch, str(date), user, "EDIT"])
            return