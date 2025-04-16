import streamlit as st
from login import login_page
from admin_dashboard import admin_dashboard
from user_page import user_page
from database import get_user_collection, get_complaints_collection
from pathlib import Path
from chatbot import chatbot_page

from operations_admin import operations_admin_page
from safety_logistics_admin import safety_logistics_admin_page
from customer_service_admin import customer_service_admin_page

st.set_page_config(page_title="Complaint Management System", layout="wide")

# Function to load CSS
def load_css():
    css_file = Path('styles.css')
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS file

load_css()

def main():
    users_collection = get_user_collection
    complaints_collection = get_complaints_collection
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to:", ["Login", "Admin Dashboard" ,"User Page","AI Helper","Operations Admin","Safety and Logistics Admin","Customer Service Admin"])

    


    if menu == "Login":
        st.sidebar.image('login.png',width=250)
        login_page(users_collection)

    elif menu == "Admin Dashboard":
        st.sidebar.image('complaint_agent.png',width=250)
        val = st.session_state.get("c_a",False) or st.session_state.get("s_a",False) or st.session_state.get("o_a",False)
        if val:
            st.warning("Higher Authority warning")
        elif "username" in st.session_state and st.session_state.get("is_admin", False) :
            admin_dashboard(complaints_collection)
        else:
            st.warning("Only admins can access this page.")

    elif menu == "User Page":
        st.sidebar.image('raillogo.png',width=250)
        if "username" in st.session_state:
            user_page(users_collection, complaints_collection)
        else:
            st.warning("Please log in to access this page.")

    elif menu == "AI Helper":
        st.sidebar.image('aibot.png',width=250)
        if "username" in st.session_state:
            chatbot_page()
        else:
            st.warning("Please log in to access this page")

    elif menu == "Operations Admin":
        #st.sidebar.image('operations.png', width=250)
        if "username" in st.session_state and st.session_state.get("o_a", False):
            operations_admin_page(complaints_collection)
        else:
            st.warning("Only Operations Department Admins can access this page.")

    elif menu == "Safety and Logistics Admin":
        #st.sidebar.image('safety.png', width=250)
        if "username" in st.session_state and st.session_state.get("s_a", False):
            safety_logistics_admin_page(complaints_collection)
        else:
            st.warning("Only Safety and Logistics Admins can access this page.")

    elif menu == "Customer Service Admin":
        #st.sidebar.image('customer_service.png', width=250)
        if "username" in st.session_state and st.session_state.get("c_a", False):
            customer_service_admin_page(complaints_collection)
        else:
            st.warning("Only Customer Service Admins can access this page.")

if __name__ == "__main__":
    main()