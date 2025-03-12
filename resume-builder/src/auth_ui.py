import streamlit as st
import json
import os
import bcrypt
from pathlib import Path

class AuthUI:
    def __init__(self):
        self.users_file = Path("data/users.json")
        self.users_file.parent.mkdir(exist_ok=True)
        if not self.users_file.exists():
            self.users_file.write_text("{}")
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        # Initialize form field states
        for key in ['login_username', 'login_password', 'reg_username', 'reg_email', 'reg_password', 'reg_confirm_password']:
            if key not in st.session_state:
                st.session_state[key] = ""
            
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            
            if username in users:
                stored_password = users[username]["password"].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
            return False
        except Exception as e:
            st.error(f"Error verifying user: {str(e)}")
            return False
            
    def create_user(self, username, password, email):
        """Create a new user"""
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
            
            # Check if username or email already exists
            for user_data in users.values():
                if user_data.get("email") == email:
                    return False
            
            if username not in users:
                # Hash the password
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                users[username] = {
                    "password": hashed.decode('utf-8'),
                    "email": email
                }
                
                with open(self.users_file, "w") as f:
                    json.dump(users, f, indent=4)
                return True
            return False
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return False
    
    def clear_form(self):
        """Clear registration form fields"""
        for key in ['reg_username', 'reg_email', 'reg_password', 'reg_confirm_password']:
            st.session_state[key] = ""
            
    def login_page(self):
        """Render the login page"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.title("Login")
            
            # Create tabs for login and registration
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            # Login tab
            with tab1:
                with st.container():
                    username = st.text_input("Username", key="login_username")
                    password = st.text_input("Password", type="password", key="login_password")
                    
                    if st.button("Login", use_container_width=True):
                        if self.verify_user(username, password):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success("Successfully logged in!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
            
            # Registration tab
            with tab2:
                with st.container():
                    reg_username = st.text_input("Username", key="reg_username")
                    reg_email = st.text_input("Email", key="reg_email")
                    reg_password = st.text_input("Password", type="password", key="reg_password")
                    reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
                    
                    if st.button("Register", use_container_width=True):
                        if not reg_username or not reg_email or not reg_password:
                            st.error("Please fill in all fields")
                        elif reg_password != reg_confirm_password:
                            st.error("Passwords do not match")
                        else:
                            if self.create_user(reg_username, reg_password, reg_email):
                                st.success("Registration successful! Please login.")
                                self.clear_form()
                            else:
                                st.error("Username or email already exists")

    def show_logout_button(self):
        """Show logout button and handle logout"""
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            return True
        return False
