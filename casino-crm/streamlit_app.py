import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Авторизація в Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gspread_credentials.json", scope)
client = gspread.authorize(creds)

# Відкриваємо таблицю
spreadsheet = client.open("CasinoCRM")
sheet = spreadsheet.sheet1

st.title("📋 Casino CRM")

with st.form("lead_form"):
    name = st.text_input("Ім'я та Прізвище")
    email = st.text_input("Email")
    phone = st.text_input("Телефон")
    platform = st.selectbox("Платформа", ["1win", "Pin-Up", "Joker", "Monro", "Cosmolot"])
    reg_date = st.date_input("Дата реєстрації")
    dep_date = st.date_input("Дата депозита")
    deposit = st.number_input("Сума депозиту", 0)
    status = st.selectbox("Статус", ["Зареєстрований", "Депозит", "FTD", "Оплачено"])
    submit = st.form_submit_button("Зберегти")

if submit:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, name, email, phone, platform, str(reg_date), str(dep_date), deposit, status])
    st.success("✅ Додано!")

# Вивід даних
data = sheet.get_all_records()
df = pd.DataFrame(data)
st.subheader("📊 Дані")
st.dataframe(df)
