import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# ✅ Required scopes
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ Fix: convert secret string to dict
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(st.secrets["GCP_SERVICE_ACCOUNT"]), scope
)

# ✅ Connect to the spreadsheet
gc = gspread.authorize(creds)
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1E9x7o_xsU67NYff2UNRtX9bwZpb9yfL2y52WofVF7f0")
entries_ws = spreadsheet.worksheet("Daily_Entries")
logs_ws = spreadsheet.worksheet("User_Logs")

# ⏺️ Check for existing entry
def get_existing_entry(branch, date):
    records = entries_ws.get_all_records()
    for i, record in enumerate(records):
        if record["Branch"] == branch and record["Date"] == date:
            return i + 2, record  # account for 1-based index and header
    return None, None

# ✏️ Check if edit is allowed within 7 days
def is_edit_allowed(record_timestamp):
    last_edit_time = datetime.strptime(record_timestamp, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_edit_time <= timedelta(days=7)

# 🟩 Submit new record
def submit_data(data):
    entries_ws.append_row(data)
    logs_ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[0], data[1], data[3], "New submission"])

# 📝 Update existing record
def update_data(row_index, updated_row):
    cell_range = f"A{row_index}:M{row_index}"
    cell_list = entries_ws.range(cell_range)
    for i, cell in enumerate(cell_list):
        cell.value = updated_row[i]
    entries_ws.update_cells(cell_list)

    logs_ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), updated_row[0], updated_row[1], updated_row[3], "Edited entry"])
