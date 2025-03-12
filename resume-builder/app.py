import streamlit as st
from src.auth_ui import AuthUI
from src.resume_builder_ui import ResumeBuilderUI

def set_page_config():
    st.set_page_config(
        page_title="AI Resume Builder",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_navigation():
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0

def main():
    set_page_config()
    initialize_navigation()
    
    # Initialize authentication
    auth = AuthUI()
    auth.initialize_session_state()
    
    # Show logout button in sidebar if logged in
    if st.session_state.logged_in:
        with st.sidebar:
            st.write(f"👤 Welcome, {st.session_state.username}!")
            if auth.show_logout_button():
                st.rerun()
    
    # Show login page if not logged in
    if not st.session_state.logged_in:
        st.title("Welcome to AI Resume Builder")
        st.write("Please login or register to create your professional resume")
        auth.login_page()
    else:
        # Initialize and render the resume builder UI
        resume_builder = ResumeBuilderUI()
        resume_builder.render()

if __name__ == "__main__":
    main()
