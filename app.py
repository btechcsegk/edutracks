import streamlit as st
from components.home_page import HomePage
from components.admin_page import AdminPage
from components.student_page import StudentPage
from components.faculty_page import FacultyPage
from database import db


def main():
    st.set_page_config(page_title="Edu Tracks",page_icon="assets/icon.png",layout="wide")

    db.createTables()
    


    with open("assets/style.css") as f:
        st.html(f"<style>{f.read()}</style>")

    if "page" not in st.session_state:
        st.session_state.page = "Home"
    def att():
        with open("assets/other_page.css") as f:
            st.html(f"<style>{f.read()}</style>")
        st.write(f"{st.session_state.uid} Logged In Successfully.")


    if st.session_state.page == "Home":
        HomePage()
    elif st.session_state.page == "Admin":
        AdminPage()
    elif st.session_state.page == "Student":
        StudentPage()
    elif st.session_state.page == "Faculty":
        FacultyPage()
        
if __name__=="__main__":
    main()