import streamlit as st
import pandas as pd
import datetime

# --- Просте збереження даних у сесії (поки без бази даних)
if 'leads' not in st.session_state:
    st.session_state.leads = []

# --- Користувачі та ролі
users = {
    "admin": {"password": "admin123", "role": "owner"},
    "manager": {"password": "manager123", "role": "manager"},
    "agent1": {"password": "agent123", "role": "agent"},
}

# --- Авторизація
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

# --- Панель CRM
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
            st.session_state.leads.append({
                "name": name,
                "email": email,
                "phone": phone,
                "telegram": telegram,
                "platform": platform,
                "manager": manager,
                "registration_date": registration_date,
                "deposit_date": deposit_date,
                "status": status,
                "cpa_amount": cpa_amount,
                "created_by": st.session_state.user
            })
            st.success("✅ Lead added successfully!")

# --- Перегляд лідів
if page == "📋 View Leads":
    st.header("📋 Lead List")

    df = pd.DataFrame(st.session_state.leads)

    # Фільтрація за роллю
    role = st.session_state.role
    user = st.session_state.user

    if role == "agent":
        df = df[df["manager"] == user]
        df = df.drop(columns=["cpa_amount"])
    elif role == "manager":
        df = df[df["manager"] == user]
        df = df.drop(columns=["cpa_amount"])
    elif role == "owner":
        pass  # бачить все

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Поки що немає даних для показу.")
