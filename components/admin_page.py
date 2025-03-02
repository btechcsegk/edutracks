import streamlit as st 
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from database import db
from utlis import utils
from st_aggrid import AgGrid, GridOptionsBuilder

def FacultyPage():
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
        # Setup AgGrid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection('single')  # Allow single row selection
        grid_options = gb.build()

        # Display AgGrid interactive table
        response = AgGrid(df, gridOptions=grid_options)
        
        def deleteFaculty(email):
            db.delete_faculty(email)
        # Get selected row data
        selected_row = response.get('selected_rows', [])
        if isinstance(selected_row,pd.DataFrame):
            name = list(selected_row['Name'])
            email = list(selected_row['Email'])
            cols = st.columns(4)
            cols[0].write(name[0])
            cols[1].write(email[0])
            cols[2].button("Update", key="update-faculty")
            cols[3].button("Delete", key="delete-faculty")

    # Add New Faculty Section
    elif selection == 'Add Faculty':
        st.header("Add New Faculty")
        
        with st.form(key='faculty_form'):
            name = st.text_input("__Enter Name__")
            email = st.text_input("__Enter Email__")
            gender = st.selectbox("__Choose Gender__",["Male","Female","Other"])
            course = st.selectbox("__Select Course__", [i[1] for i in db.get_all_courses()])
            course_dict = {i[1]:i[0] for i in db.get_all_courses()}
            submit_button = st.form_submit_button(label='Add Faculty')

        if submit_button:
            # Create a new faculty entry
            db.create_faculty(email,name,gender,course_dict[course])
            st.success(f"{name} added successfully.")

def AdminPage():
    with open("assets/admin_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    st.header("⚙️ ADMIN DASHBOARD")
    
    st.sidebar.subheader("Admin Menu")
    choice = st.sidebar.radio("Choose Operation",["👨🏻‍🎓 Student","👨🏻‍💼 Faculty","🏙️ Department"],label_visibility="collapsed",key="admin-menu")
    
    if choice.split()[1] == "Student":
        st.subheader("Student Details")
        col1,col2,col3 = st.columns(3)
        col1.metric(label="Total Students", value=2000)
        col2.metric(label="Number of Girls", value=765)
        col3.metric(label="Number of Boys", value=1235)
        style_metric_cards()
        with st.expander("Student List"):
            my_list = [i for i in range(1,101)]
            df = pd.DataFrame({"Roll Number":my_list,"Roll Calls":my_list})
            st.dataframe(df)
        st.subheader("Add Student")
        roll = st.text_input("__Enter Roll Number__",placeholder="2204921540027")
        name = st.text_input("__Enter Name__",placeholder="Anshu")
        passwd = st.text_input("__Enter Password__",type="password")
        dob = st.date_input("__DOB__")
        phone = st.text_input("__Enter Phone Number__",placeholder="+91 XXXXXXXXXX")
        with st.columns(5)[2]:
            st.button("Add",key="add-student")
    elif choice.split()[1] == "Faculty":
        st.subheader("Faculty Details")
        col1,col2,col3 = st.columns(3)
        col1.metric(label="Total Faculties", value=db.getTotalFaculties())
        col2.metric(label="Female Faculties", value=db.getTotalFemaleFaculties())
        col3.metric(label="Male Faculties", value=db.getTotalMaleFaculties())
        style_metric_cards()
        FacultyPage()
        # with st.expander("Faculty List"):
        #     my_list = [i for i in range(1,101)]
        #     df = pd.DataFrame({"Faculty Id":my_list,"Roll Calls":my_list})
        #     st.dataframe(df)
        # st.subheader("Add Faculty")
        # roll = st.text_input("__Enter Faculty Id__",placeholder="2204921540027")
        # name = st.text_input("__Enter Name__",placeholder="Anshu")
        # passwd = st.text_input("__Enter Password__",type="password")
        # phone = st.text_input("__Enter Phone Number__",placeholder="+91 XXXXXXXXXX")
        # with st.columns(5)[2]:
        #     st.button("Add",key="add-faculty")
    elif choice.split()[1] == "Department":
        st.subheader("Department Details")
        col1,col2 = st.columns(2)
        col1.metric(label="__Total Courses Offered__", value=db.getTotalCourses())
        col2.metric(label="__Total Branches__", value=db.getTotalDepartments())
        style_metric_cards()
        
        sb_dept = st.selectbox("Select Department",[ i[1] for i in db.get_all_departments()])
        
        if sb_dept=="CSE":
            with st.expander("Courses Offered"):
                c_list = ["Introduction to Programming","Data Structures and Algorithms","Database Management Systems"]
                st.table({"Course List":c_list})
        
        dept_col,cr_col=st.columns(2)
        with dept_col:
            st.subheader("Add Department")
            dept_id = st.text_input("Enter Derpatment Id")
            dept_name = st.text_input("Enter Derpatment Name")
            with st.columns(3)[1]:
                st.button("Add Department")
        with cr_col:
            st.subheader("Add Course")
            c_id = st.text_input("Enter Course Id")
            c_name = st.text_input("Enter Course Name")
            with st.columns(3)[1]:
                st.button("Add Course")
    else:
        st.write("Choose a field")