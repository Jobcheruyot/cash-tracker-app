import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(st.secrets["GCP_SERVICE_ACCOUNT"]), scope
)
gc = gspread.authorize(creds)
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1E9x7o_xsU67NYff2UNRtX9bwZpb9yfL2y52WofVF7f0")
entries_ws = spreadsheet.worksheet("Daily_Entries")
logs_ws = spreadsheet.worksheet("User_Logs")

def get_existing_entry(branch, date):
    records = entries_ws.get_all_records()
    for i, record in enumerate(records):
        if record["Branch"] == branch and record["Date"] == date:
            return i + 2, record
    return None, None

def is_edit_allowed(timestamp):
    ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - ts <= timedelta(days=7)

def submit_data(data):
    entries_ws.append_row(data)
    logs_ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[0], data[1], data[3], "New submission"])

def update_data(row_index, data):
    cell_range = f"A{row_index}:N{row_index}"
    cells = entries_ws.range(cell_range)
    for i, cell in enumerate(cells):
        cell.value = data[i]
    entries_ws.update_cells(cells)
    logs_ws.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[0], data[1], data[3], "Edited entry"])
