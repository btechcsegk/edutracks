import streamlit as st 
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from database import db
from components import home_page
from streamlit_autorefresh import st_autorefresh

def FacultySection():
    faculties = db.get_all_faculty()
    course_dict = {i[0]:i[1] for i in db.get_all_courses()}
    data = {
        'Name': [i[1] for i in faculties],
        'Gender': [i[2] for i in faculties],
        'Email': [i[0] for i in faculties],
        'Course': [course_dict[i[3]] for i in faculties]
    }
    df = pd.DataFrame(data)
    
    # Sidebar Navigation
    sidebar_options = ['View Faculty', 'Add Faculty']
    st.sidebar.markdown("### :rainbow[Faculty Operations]")
    selection = st.sidebar.radio("Select Option", sidebar_options,label_visibility="collapsed",key="faculty-operation-list")

    # View Faculty Section
    if selection == 'View Faculty':
        st.header("Faculty List")
        st.table(data)
        
    elif selection == 'Add Faculty':
        st.header("Add New Faculty")
        fac_form = st.container(key="fac-form")
        name = fac_form.text_input("__Enter Name__")
        email = fac_form.text_input("__Enter Email__")
        gender = fac_form.selectbox("__Choose Gender__",["Male","Female","Other"])
        course = fac_form.selectbox("__Select Course__", [i[1] for i in db.get_all_courses()])
        course_dict = {i[1]:i[0] for i in db.get_all_courses()}
        submit_button = fac_form.button(label='Add Faculty')

        if submit_button:
            # Create a new faculty entry
            db.create_faculty(email,name,gender,course_dict[course])
            st.success(f"{name} added successfully.")

def AdminPage():
    with open("assets/admin_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    st.header("⚙️ ADMIN DASHBOARD")
    
    st.sidebar.subheader("Admin Menu")
    choice = st.sidebar.radio("Choose Operation",["👨🏻‍🎓 Student","👨🏻‍💼 Faculty","🏙️ Department","🔒 Logout"],label_visibility="collapsed",key="admin-menu")
    
    if choice.split()[1] == "Student":
        st.subheader("Student Details")
        col1,col2,col3 = st.columns(3)
        col1.metric(label="Total Students", value=db.get_total_students())
        col2.metric(label="Number of Girls", value=db.get_total_female_students())
        col3.metric(label="Number of Boys", value=db.get_total_male_students())
        style_metric_cards()
        stu_id = [i[0] for i in db.get_all_students()]
        stu_name = [i[1] for i in db.get_all_students()]
        stu_dob = [i[2] for i in db.get_all_students()]
        stu_gen = [i[3] for i in db.get_all_students()]
        st.subheader("Enroll Student")
        roll = st.text_input("__Enter Roll Number__",placeholder="2204921540027")
        name = st.text_input("__Enter Name__",placeholder="Anshu")
        passwd = st.text_input("__Enter Password__",type="password")
        dob = st.date_input("__DOB__")
        gender = st.selectbox("__Select Gender__",["Male", "Female", "Other"])
        with st.columns(5)[2]:
            if st.button("Add",key="add-student"):
                db.create_student(roll,name,dob,gender)
        
        
        st.subheader("Student List")
        st.table({"Roll Number":stu_id, "Name": stu_name, "Gender": stu_gen, "DOB": stu_dob})
        
        
    elif choice.split()[1] == "Faculty":
        st.subheader("Faculty Details")
        col1,col2,col3 = st.columns(3)
        col1.metric(label="Total Faculties", value=db.get_total_faculties())
        col2.metric(label="Female Faculties", value=db.get_total_female_faculties())
        col3.metric(label="Male Faculties", value=db.get_total_male_faculties())
        style_metric_cards()
        FacultySection()
        
    elif choice.split()[1] == "Department":
        st.subheader("Department Details")
        col1,col2 = st.columns(2)
        col1.metric(label="__Total Courses Offered__", value=db.get_total_courses())
        col2.metric(label="__Total Branches__", value=db.get_total_branches())
        style_metric_cards()
        c_dict = {i[1]:i[0] for i in db.get_all_courses()}
        sb_course = st.selectbox("Select Course", c_dict.keys())
        st.subheader(f"Branches in {sb_course}")
        b_list = [i[1] for i in db.get_all_branches_by_course(c_dict[sb_course])]
        st.table({"Course List":b_list})
        
        cr_col,br_col=st.columns(2)
        with cr_col:
            st.subheader("Add Course")
            c_id = st.text_input("Enter Course Id")
            c_name = st.text_input("Enter Course Name")
            c_duration  = st.text_input("Enter Course Duration")
            with st.columns(3)[1]:
                if st.button("Add Course"):
                    
        with br_col:
            st.subheader("Add Branch")
            dept_id = st.text_input("Enter Branch Code")
            dept_name = st.text_input("Enter Branch Name")
            _id = st.selectbox("Choose Course",c_dict.keys())
            temp_id = c_dict[_id]
            with st.columns(3)[1]:
                if st.button("Add Branch"):
                    db.create_branch(dept_id,dept_name,temp_id) 
    else:
        st.session_state.page = "Home"
        st_autorefresh()