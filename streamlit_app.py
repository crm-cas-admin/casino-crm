
import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Авторизація Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
import os

# Читаємо з секретного ENV
creds_json = os.environ.get("GSPREAD_CREDENTIALS")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# --- Назва таблиці
SHEET_NAME = "CasinoCRM"
try:
    sheet = client.open(SHEET_NAME).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    sheet = client.create(SHEET_NAME).sheet1
    sheet.append_row(["name", "email", "phone", "telegram", "platform", "manager", "registration_date", "deposit_date", "status", "cpa_amount", "created_by"])

# --- Авторизація користувачів
users = {
    "admin": {"password": "admin123", "role": "owner"},
    "manager": {"password": "manager123", "role": "manager"},
    "agent1": {"password": "agent123", "role": "agent"},
}

def login():
    st.title("CRM Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.user = username
            st.session_state.role = users[username]["role"]
        else:
            st.error("❌ Invalid credentials")

if "user" not in st.session_state:
    login()
    st.stop()

st.sidebar.success(f"Logged in as: {st.session_state.user} ({st.session_state.role})")
page = st.sidebar.radio("Go to", ["➕ Add Lead", "📋 View Leads"])

# --- Додавання ліда
if page == "➕ Add Lead":
    st.header("➕ Add New Lead")
    with st.form("lead_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        telegram = st.text_input("Telegram")
        platform = st.selectbox("Platform", ["1win", "Pin-Up", "Slotum", "BetWinner", "Booi"])
        manager = st.selectbox("Manager", ["manager", "agent1"])
        registration_date = st.date_input("Registration Date", datetime.date.today())
        deposit_date = st.date_input("Deposit Date")
        status = st.selectbox("Status", ["Registered", "Deposited", "FTD", "Paid"])
        cpa_amount = st.number_input("CPA Amount", value=0.0)
        submitted = st.form_submit_button("Submit")

        if submitted:
            new_row = [
                name, email, phone, telegram, platform, manager,
                registration_date.strftime("%Y-%m-%d"),
                deposit_date.strftime("%Y-%m-%d"),
                status, cpa_amount, st.session_state.user
            ]
            sheet.append_row(new_row)
            st.success("✅ Lead added to Google Sheets!")

# --- Перегляд
if page == "📋 View Leads":
    st.header("📋 Lead List")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    role = st.session_state.role
    user = st.session_state.user

    if role in ["manager", "agent"]:
        df = df[df["manager"] == user]
        if "cpa_amount" in df.columns:
            df = df.drop(columns=["cpa_amount"])

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Поки що немає записів.")
