import streamlit as st

def login_page(users_collection):
    st.title("Login / Signup")
    
    
    main_tab, image_tab = st.columns(2)
    # Dropdown for login/signup or admin

    with main_tab:

        user_action = st.selectbox("Select Action", ["Login / Signup", "Login as Admin"])

        # Login / Signup for Users
        if user_action == "Login / Signup":
            tab1, tab2 = st.tabs(["Login", "Signup"])

            # Login Tab
            with tab1:
                username = st.text_input("Username", key="username_login")
                password = st.text_input("Password", type="password", key="password_login")

                if st.button("Login"):
                    user = users_collection.find_one({"username": username, "password": password})
                    if user:
                        st.session_state.username = username
                        st.session_state.is_admin = False
                        st.success("Login successful!")
                        st.balloons()
                    else:
                        st.error("Invalid username or password.")

            # Signup Tab
            with tab2:
                new_username = st.text_input("New Username", key="new_username_signup")
                new_password = st.text_input("New Password", type="password", key="new_password_signup")
                if st.button("Signup"):
                    if users_collection.find_one({"irctc_id": new_username}):
                        st.error("Username already exists. Please choose another.")
                    else:
                        users_collection.insert_one({"username": new_username, "password": new_password, "is_admin": False})
                        st.success("Account created successfully!")

        # Login for Admins
        elif user_action == "Login as Admin":
            admin_username = st.text_input("Admin Username", key="admin_username")
            admin_password = st.text_input("Admin Password", type="password", key="admin_password")

            if st.button("Admin Login"):
                admin = users_collection.find_one({"username": admin_username, "password": admin_password, "is_admin": True})
                if admin:
                    st.session_state.username = admin_username
                    if admin['c_a'] is True:
                        st.session_state.c_a = True
                    elif admin['s_a'] is True:
                        st.session_state.s_a = True
                    elif admin['o_a'] is True:
                        st.session_state.o_a = True
                    else:
                        st.session_state.is_admin = True
                    st.success("Admin login successful!")
                else:
                    st.error("Invalid admin credentials.")

    with image_tab:
        st.image('vvce-logo.png',width=300)
