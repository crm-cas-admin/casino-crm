import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Авторизація
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("gspread_credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Підключення до Google Таблиці
spreadsheet = client.open("CasinoCRM")
worksheet = spreadsheet.sheet1

# Завантаження даних
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Вивід у Streamlit
st.title("Casino CRM Viewer")
st.dataframe(df)
