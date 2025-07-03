
import streamlit as st
import pandas as pd
import datetime

# --- Ініціалізація сесії
if 'leads' not in st.session_state:
    st.session_state.leads = []

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

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

# --- Панель навігації
st.sidebar.success(f"Logged in as: {st.session_state.user} ({st.session_state.role})")
page = st.sidebar.radio("Go to", ["➕ Add Lead", "📋 View Leads"])

# --- Форма додавання/редагування ліда
def lead_form(index=None):
    is_edit = index is not None
    st.header("✏️ Edit Lead" if is_edit else "➕ Add New Lead")

    if is_edit:
        lead = st.session_state.leads[index]
    else:
        lead = {
            "name": "",
            "email": "",
            "phone": "",
            "telegram": "",
            "platform": "1win",
            "manager": "manager",
            "registration_date": datetime.date.today(),
            "deposit_date": datetime.date.today(),
            "status": "Registered",
            "cpa_amount": 0.0,
            "created_by": st.session_state.user
        }

    with st.form("lead_form"):
        name = st.text_input("Full Name", value=lead["name"])
        email = st.text_input("Email", value=lead["email"])
        phone = st.text_input("Phone", value=lead["phone"])
        telegram = st.text_input("Telegram", value=lead["telegram"])
        platform = st.selectbox("Platform", ["1win", "Pin-Up", "Slotum", "BetWinner", "Booi"], index=0)
        manager = st.selectbox("Manager", ["manager", "agent1"], index=0)
        registration_date = st.date_input("Registration Date", value=lead["registration_date"])
        deposit_date = st.date_input("Deposit Date", value=lead["deposit_date"])
        status = st.selectbox("Status", ["Registered", "Deposited", "FTD", "Paid"], index=0)
        cpa_amount = st.number_input("CPA Amount", value=float(lead["cpa_amount"]))
        submitted = st.form_submit_button("Save")

        if submitted:
            updated_lead = {
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
                "created_by": st.session_state.user if not is_edit else lead["created_by"]
            }
            if is_edit:
                st.session_state.leads[index] = updated_lead
                st.success("✅ Lead updated!")
                st.session_state.edit_index = None
            else:
                st.session_state.leads.append(updated_lead)
                st.success("✅ Lead added!")

# --- Додавання ліда
if page == "➕ Add Lead":
    lead_form()

# --- Перегляд лідів + редагування
if page == "📋 View Leads":
    st.header("📋 Lead List")
    df = pd.DataFrame(st.session_state.leads)
    role = st.session_state.role
    user = st.session_state.user

    if role in ["manager", "agent"]:
        df = df[df["manager"] == user]
        df = df.drop(columns=["cpa_amount"])

    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"{row['name']} ({row['platform']})"):
                st.write(row.to_frame().T)
                if role == "owner" or row["manager"] == user:
                    if st.button("✏️ Edit", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()
    else:
        st.info("Поки що немає даних для показу.")

# --- Якщо натиснули редагування
if st.session_state.edit_index is not None:
    lead_form(index=st.session_state.edit_index)
