import streamlit as st 
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from database import db
from datasource import remoteDataSource
from components import home_page
from models import user
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

def FacultySection():
    faculties = db.get_all_faculty()
    facultie_with_lec = db.get_lecture_with_fac()
    course_dict = {i[0]:i[1] for i in db.get_all_courses()}
    data = {
        'Name': [i[1] for i in faculties],
        'Gender': [i[2] for i in faculties],
        'Email': [i[0] for i in faculties],
        'Course': [course_dict[i[3]] for i in faculties]
    }
    lec_data = {
        'Name': [i[0] for i in facultie_with_lec],
        'Email': [i[1] for i in facultie_with_lec],
        'Subject Code': [i[2] for i in facultie_with_lec]
    }
    df = pd.DataFrame(data)
    
    # Sidebar Navigation
    sidebar_options = ['View Faculty', 'Add Faculty', 'Assign Lecture']
    st.sidebar.markdown("### :rainbow[Faculty Operations]")
    selection = st.sidebar.radio("Select Option", sidebar_options,label_visibility="collapsed",key="faculty-operation-list")

    # View Faculty Section
    if selection == 'View Faculty':
        st.header("Faculty List")
        st.table(data)
        st.header("Lecture List")
        st.table(lec_data)
        
    elif selection == 'Add Faculty':
        st.header("Add New Faculty")
        fac_form = st.container(key="fac-form")
        name = fac_form.text_input("__Enter Name__")
        email = fac_form.text_input("__Enter Email__")
        passwd = fac_form.text_input("__Set Password__")
        gender = fac_form.selectbox("__Choose Gender__",["Male","Female","Other"])
        course = fac_form.selectbox("__Select Course__", [i[1] for i in db.get_all_courses()])
        course_dict = {i[1]:i[0] for i in db.get_all_courses()}
        submit_button = fac_form.button(label='Add Faculty')

        if submit_button:
            db.create_faculty(email,name,gender,course_dict[course])
            new_user=user.User()
            new_user.username=email
            new_user.password=passwd
            new_user.name=name
            new_user.role="Faculty"
            remoteDataSource.addUser(new_user)
            st.success(f"{name} added successfully.")
    else:
        sub_dict = {i[1]:i[0] for i in db.get_all_subjects()}
        st.write("## Assign Lecture to Faculty")
        fac = st.selectbox("Select a faculty",data["Email"])
        sub = st.selectbox("Select a subject", sub_dict.keys())
        if st.button("Assign Lecture"):
            db.create_lecture(fac,sub_dict[sub])

def departmentSection(c_dict):
     # Sidebar Navigation
    sidebar_options = ['View Course', 'Add Course', 'Add Branch', 'Add Subject']
    st.sidebar.markdown("### :rainbow[Department Operations]")
    selection = st.sidebar.radio("Select Option", sidebar_options,label_visibility="collapsed",key="faculty-operation-list")
    
    if selection == 'View Course':
        sb_course = st.selectbox("Select Course", c_dict.keys())
        st.subheader(f"Branches in {sb_course}")
        if len(c_dict)>0:
            b_list = [i[1] for i in db.get_all_branches_by_course(c_dict[sb_course])]
            st.table({"Course List":b_list})
    
    elif selection == 'Add Branch':
        status = st.empty()
        st.subheader("Add Branch")
        dept_id = st.text_input("Enter Branch Code")
        dept_name = st.text_input("Enter Branch Name")
        _id = st.selectbox("Choose Course",c_dict.keys())
        with st.columns(3)[1]:
            if st.button("Add Branch"):
                db.create_branch(dept_id,dept_name,c_dict[_id])
                status.success("Course Added Successfully")
    elif selection == 'Add Course':
        status = st.empty()
        st.subheader("Add Course")
        c_id = st.text_input("Enter Course Id")
        c_name = st.text_input("Enter Course Name")
        c_duration  = st.text_input("Enter Course Duration", placeholder="4")
        with st.columns(3)[1]:
            if st.button("Add Course"):
                db.create_course(c_id,c_name,c_duration)
                status.success("Course Added Successfully")
    
    else:
        status = st.empty()
        st.subheader("Add Subject")
        sub_id = st.text_input("Enter Subject Code")
        sub_name = st.text_input("Enter Subject Name")
        c_id =  st.selectbox("__Select Course__", c_dict.keys())
        sem =  st.selectbox("__Select Semester__", [i[0] for i in db.get_all_semester()])
        if len(c_dict)>0:
            b_id = st.selectbox("__Select Branch__",[ i[1] for i in db.get_all_branches_by_course(c_dict[c_id])])
            b_dict = { i[1]:i[0] for i in db.get_all_branches_by_course(c_dict[c_id])}
        with st.columns(3)[1]:
            if st.button("Add Subject"):
                db.create_subject(sub_id,sub_name,c_dict[c_id],sem,b_dict[b_id])
                status.success("Subject Added Successfully")
                
def studentSection(c_dict):
    stu_id = [i[0] for i in db.get_all_students()]
    stu_name = [i[1] for i in db.get_all_students()]
    stu_dob = [i[2] for i in db.get_all_students()]
    stu_gen = [i[3] for i in db.get_all_students()]
    
     # Sidebar Navigation
    sidebar_options = ['View Student', 'Enroll Student']
    st.sidebar.markdown("### :rainbow[Student Operations]")
    selection = st.sidebar.radio("Select Option", sidebar_options,label_visibility="collapsed",key="faculty-operation-list")
    
    
    if selection == 'View Student':
        st.subheader("Student List")
        st.table({"Roll Number":stu_id, "Name": stu_name, "Gender": stu_gen, "DOB": stu_dob})
    else:
        status = st.empty()
        st.subheader("Enroll Student")
        roll = st.text_input("__Enter Roll Number__",placeholder="2204921540027")
        name = st.text_input("__Enter Name__",placeholder="Anshu")
        passwd = st.text_input("__Enter Password__",type="password")
        dob = st.date_input("__DOB__",None,datetime(2000,1,1),datetime.now())
        gender = st.selectbox("__Select Gender__",["Male", "Female", "Other"])
        c_id =  st.selectbox("__Select Course__", c_dict.keys())
        sem =  st.selectbox("__Select Semester__", [i[0] for i in db.get_all_semester()])
        if len(c_dict)>0:
            b_id = st.selectbox("__Select Branch__",[ i[1] for i in db.get_all_branches_by_course(c_dict[c_id])])
            b_dict = { i[1]:i[0] for i in db.get_all_branches_by_course(c_dict[c_id])}
        with st.columns(5)[2]:
            if st.button("Add",key="add-student"):
                db.create_student(roll,name,dob,gender)
                db.create_enrollment(roll, c_dict[c_id], b_dict[b_id],sem)
                new_user=user.User()
                new_user.username=roll
                new_user.password=passwd
                new_user.name=name
                new_user.role="Student"
                remoteDataSource.addUser(new_user)
                status.success(f"{name} is added successfuly.")
    
def AdminPage():
    with open("assets/admin_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    st.header("⚙️ ADMIN DASHBOARD")
    
    st.sidebar.subheader("Admin Menu")
    choice = st.sidebar.radio("Choose Operation",["👨🏻‍🎓 Student","👨🏻‍💼 Faculty","🏙️ Department","🔒 Logout"],label_visibility="collapsed",key="admin-menu")
    
    if choice.split()[1] == "Student":
        c_dict = {i[1]:i[0] for i in db.get_all_courses()}
        st.subheader("Student Details")
        col1,col2,col3 = st.columns(3)
        col1.metric(label="Total Students", value=db.get_total_students())
        col2.metric(label="Number of Girls", value=db.get_total_female_students())
        col3.metric(label="Number of Boys", value=db.get_total_male_students())
        style_metric_cards() 
        studentSection(c_dict)
        
        
        
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
        
        departmentSection(c_dict)
            
                    
    else:
        st.session_state.page = "Home"
        st_autorefresh()