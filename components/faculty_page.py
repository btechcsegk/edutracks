import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import db
from st_aggrid import AgGrid, GridOptionsBuilder
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def viewAnalytics():
    main_col1,main_col2 = st.columns([3,2],gap="medium")
    with main_col1:
        col1,col2= st.columns(2)
        with col1:
            course_list = {i[1]:i[0] for i in db.get_all_courses()}
            course = st.selectbox("Course List",course_list.keys(), label_visibility="collapsed")
            sems = {
                "Sem 1": 1,
                "Sem 2": 2,
                "Sem 3": 3,
                "Sem 4": 4,
                "Sem 5": 5,
                "Sem 6": 6,
                "Sem 7": 7,
                "Sem 8": 8
            }
            sem_list = list(sems.keys())
            if course=="BCA":
                sem_list.pop()
                sem_list.pop()
            
            sem = st.selectbox("Semester List",sem_list, index=5, label_visibility="collapsed")
            
        
        with col2:
            con = st.container(key="stu-con")
            con.image("assets/student.png",width=100)
            con.markdown(f"### {db.get_total_students_by_semester(course_list[course],sems[sem])} \n Student count")
            
        
        an_box = st.container(key="an-box")
        # Title
        an_box.header("Number of Students in each exam")
        
        if db.get_exams_data() is not None:
            exam_data = db.get_exams_data()
            exams = [i[0] for i in exam_data]
            no_of_stu = [i[1] for i in exam_data]
            df = pd.DataFrame({'Exams': exams,'Students Appeared': no_of_stu})
            col_list=list(df.columns)
            fig = df.plot(kind='bar',x=col_list[0],y=col_list[1:])
            plt.xticks(rotation=20)
            an_box.pyplot(fig.figure)
        else:
            an_box.write("No Exams Found")
                
                
    with main_col2:
        st.subheader("Best Performers")
        c1,c2= st.columns(2)
        with c1:
            mm_male = [i[1] for i in db.best_in_marks_male_by_sem()]
            mm_female = [i[1] for i in db.best_in_marks_female_by_sem()]
            mm_male_list = [i[0] for i in db.best_in_marks_male_by_sem()]
            mm_female_list = [i[0] for i in db.best_in_marks_female_by_sem()]
            
            ma = {i[0]:i[1] for i in db.best_in_att_male_by_sem(sems[sem])}
            fa = {i[0]:i[1] for i in db.best_in_att_female_by_sem(sems[sem])}
            
            if mm_male[0] is None:
                mm_male=[0]
            if mm_female[0] is None:
                mm_female=[0]
            if mm_male_list[0] is None:
                mm_male_list=["None"]
            if mm_female_list[0] is None:
                mm_female_list=["None"]
                
            if fa.keys().__contains__(None):
                fa.clear()
                fa["None"]=0
            if ma.keys().__contains__(None):
                ma.clear()
                ma["None"]=0
                
            mcon1 = st.container(key="stu-perf-1")
            mcon1.image("assets/bp.png",width=100)
            mcon1.markdown(f"#### {mm_male[0] if len(mm_male)>0 else 0} ({",".join(mm_male_list) if len(mm_male_list)>0 else "None"})\nBest In Marks")
            mcon2 = st.container(key="stu-att-1")
            mcon2.image("assets/bp1.png",width=100)
            mcon2.markdown(f"#### {list(ma.values())[0]} ({",".join(ma.keys())})\nBest In Attendance")
        with c2:
            mcon1 = st.container(key="stu-perf-2")
            mcon1.image("assets/gp.png",width=100)
            mcon1.markdown(f"#### {mm_female[0]} ({",".join(mm_female_list)})\nBest In Marks")
            mcon2 = st.container(key="stu-att-2")
            mcon2.image("assets/gp1.png",width=100)
            mcon2.markdown(f"#### {list(fa.values())[0]} ({",".join(fa.keys())})\nBest In Attendance")
        
def getFetchOne(val):
    if val is not None:
        return val[0] 
def getFetchOneInt(val):
    if val is not None:
        return val[0]
    return 0 
def set_height(df):
        MIN_HEIGHT = 50
        MAX_HEIGHT = 800
        ROW_HEIGHT = 50
        return min(MIN_HEIGHT + len(df) * ROW_HEIGHT, MAX_HEIGHT)
        
def markAttendance():
    st.subheader("Mark Attendance")
    sub_dictk = {i[0]:i[1] for i in db.get_all_subjects()} 
    sub_dictv = {i[1]:i[0] for i in db.get_all_subjects()} 
    sub_list = [i[0] for i in db.get_all_sub_by_fac_id(st.session_state.uid)]
    sub_id = st.selectbox("Choose a subject to mark attendance",[sub_dictk[i] for i in sub_list])
    sel_sub_id = sub_dictv[sub_id]
    total_att = db.get_total_att_by_sub_id(sel_sub_id)
    curr_att = lambda x,y: db.get_obtained_att_by_sub_and_stu_id(x,y)
    
    if getFetchOne(total_att) is None:
        total_att = 0
    else:
        total_att = getFetchOne(total_att)
    inp_col, btn_col = st.columns([3,1])
    att_value = int(inp_col.text_input("Total Attendence", value=f"{total_att}"))
    if total_att!=0:
        if btn_col.button("Update",key="btn-upd-tot"):
            db.update_total_attendance(sel_sub_id, att_value)
    else:
        if btn_col.button("Add",key="btn-upd-tot"):
            db.add_total_attendance(sel_sub_id, att_value)
        
    

    # Sample data
    sub_branch = {i[0]:i[4] for i in db.get_all_subjects()} 
    sub_sem = {i[0]:i[3] for i in db.get_all_subjects()} 
    stu_list = db.get_student_list_by_branch(sub_branch[sel_sub_id],sub_sem[sel_sub_id])
    
    df = pd.DataFrame({
        'Roll No': [i[0] for i in stu_list],
        'Name': [i[1] for i in stu_list],
        'Obtained': [getFetchOneInt(curr_att(sel_sub_id,i[0])) for i in stu_list],
        'Total': [total_att for i in range(len(stu_list))]
    })

    # Configure grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    grid_options = gb.build()


    
    # Display the grid
    grid_return = AgGrid(df, gridOptions=grid_options, 
                         theme='alpine', allow_unsafe_jscode=True, 
                         fit_columns_on_grid_load=True, 
                         reload_data=False,
                         height=set_height(df))
    
    checked_row = grid_return['selected_rows']
    
 
    if isinstance(checked_row, pd.DataFrame):
        r = checked_row['Roll No'].iloc[0]
        o = checked_row['Obtained'].iloc[0]
        t = checked_row['Total'].iloc[0]
    
        cols = st.columns([1,1,1,2])
        
        cols[0].write("__Roll No__")
        cols[0].write(f"{r}")
        cols[1].write(f"__Obtained Attendance__")
        temp_att = cols[1].text_input("_",value=f"{o}",label_visibility="collapsed")
        cols[2].write(f"__Total Attendance__")
        cols[2].write(f"{t}")
        cols[3].write(f"__Action__")
        
        checkStu = db.checkin_attendance_list_by_id(r,sel_sub_id)
        if getFetchOneInt(checkStu) != 0:
            if cols[3].button("Update Attendance",key="update-att"):
                db.update_attendance_by_id(int(temp_att),r,sel_sub_id)
        else:
            if cols[3].button("Add Attendance",key="insert-att"):
                db.insert_attendance_by_id(int(temp_att),r,sel_sub_id)
        # st.write(checked_row['Roll No'].iloc[0])
        
    

def manageMarks():
    st.subheader("Manage Marks")
    sub_dictk = {i[0]:i[1] for i in db.get_all_subjects()} 
    sub_dictv = {i[1]:i[0] for i in db.get_all_subjects()} 
    sub_list = [i[0] for i in db.get_all_sub_by_fac_id(st.session_state.uid)]
    sub_id = st.selectbox("Choose a subject to manage marks",[sub_dictk[i] for i in sub_list])
    # total_att = db.get_total_marks_by_sub_id(sub_dictv[sub_id])
    # curr_att = db.get_obtained_att_by_sub_and_stu_id('BCS601',2204921540060)
    
    # inp_col, btn_col = st.columns([3,1])
    # att_value = inp_col.text_input("Total Attendence", placeholder=f"{getFetchOne(total_att)}")
    # update_tot = btn_col.button("Update",key="btn-upd-tot")
        
    sel_sub = sub_dictv[sub_id]
    exam_list = db.get_exams_by_sub_id(sel_sub)
    if exam_list is not None:
        if len(exam_list)>0:
            sub_branch = {i[0]:i[4] for i in db.get_all_subjects()} 
            sub_sem = {i[0]:i[3] for i in db.get_all_subjects()} 
            # Sample data
            stu_list = db.get_student_list_by_branch(sub_branch[sel_sub],sub_sem[sel_sub])
            exam_dict = {i[1]:i[0] for i in exam_list}
            sel_exam = st.selectbox("Select Exam", exam_dict.keys())
            tot_marks = db.get_total_marks_by_exam_id(exam_dict[sel_exam])
            st.text_input("Total Marks", value=getFetchOneInt(tot_marks) ,disabled=True)
            
            df = pd.DataFrame({
                'Roll No': [i[0] for i in stu_list],
                'Name': [i[1] for i in stu_list]
            })

            # Configure grid options
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(selection_mode='single', use_checkbox=True)
            grid_options = gb.build()


            
            # Display the grid
            grid_return = AgGrid(df, gridOptions=grid_options, 
                                theme='alpine', allow_unsafe_jscode=True, 
                                fit_columns_on_grid_load=True, 
                                reload_data=False,
                                height=set_height(df))
            
            checked_row = grid_return['selected_rows']
            
            if isinstance(checked_row, pd.DataFrame):
                roll_no = checked_row['Roll No'].iloc[0]
                name = checked_row['Name'].iloc[0]
                cols = st.columns(4)
                cols[0].markdown(f"##### {roll_no}")
                cols[1].markdown(f"##### {name}")
                ob_marks = db.get_mark_by_id(roll_no,exam_dict[sel_exam])
                marks = int(cols[2].text_input("Enter obtained marks", value=getFetchOneInt(ob_marks), label_visibility="collapsed"))
                
                checkStuInExam = getFetchOneInt(db.checkin_mark_list_by_id(roll_no,exam_dict[sel_exam]))
                if checkStuInExam == 0:
                    if cols[3].button(f"Save Mark", key="btn-save-mark"):
                        db.add_mark(roll_no,exam_dict[sel_exam],marks)
                else:
                    if cols[3].button(f"Update Mark", key="btn-save-mark"):
                        db.update_mark(roll_no,exam_dict[sel_exam],marks)
        else:
            st.write("##### `No Exams Found for this subject`")
    else:
        st.write("##### `No Exams Found for this subject`")
    
    
    # st.write(checked_row['Roll No'].iloc[0])



def addExam():
    st.write("#### Add Exam")
    e_id = st.text_input("Enter Exam Code")
    e_name = st.text_input("Enter Exam Name")
    sub_list = [i[0] for i in db.get_all_sub_by_fac_id(st.session_state.uid)]
    sub_id = st.selectbox("Choose Subject", sub_list)
    e_marks = int(st.text_input("Enter Total Marks",value=0))
    
    if st.button("Add Exam"):
        db.add_exam(e_id,e_name,e_marks,sub_id)
    
    
    
    
    
def FacultyPage():
    with open("assets/faculty_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    sidebar_options = ['View Analytics', 'Mark Attendance', 'Manage Marks', 'Add Exam', 'Communicate']
    st.sidebar.markdown("### Faculty Options")
    selection = st.sidebar.radio("Select Option", sidebar_options,label_visibility="collapsed",key="faculty-operation-list")
    
    if selection == "View Analytics":
        viewAnalytics()
    elif selection == "Mark Attendance":
        markAttendance()
    elif selection == "Manage Marks":
        manageMarks()
    elif selection == "Add Exam":
        addExam()
    else:
        st.write("# Parent Communication")
        
        uid = int(st.text_input("__Enter Student Roll No__",value=0))
        email = st.text_input("__Enter Parent Email Id__")
        mark_data =db.get_marks_subject_wise(uid) if db.get_marks_subject_wise(uid) is not None else []
        
        exams = [i[0] for i in mark_data if len(mark_data)!=0]
        marks = [i[1] for i in mark_data if len(mark_data)!=0]
        tmarks = [i[2] for i in mark_data if len(mark_data)!=0]

        # Email Configuration
        SMTP_SERVER = "smtp.gmail.com"  # Change if using another provider
        SMTP_PORT = 587
        SENDER_EMAIL = "preplyft@gmail.com"  # Replace with your email
        SENDER_PASSWORD = "fxmtbparjojuxxvv"  # Replace with your App Password
        RECIPIENT_EMAIL = email  # Replace with recipient email


        # Create HTML Table
        html_table = """
        <html>
        <head>
            <style>
                table {border-collapse: collapse; width: 50%; font-family: Arial, sans-serif;}
                th, td {border: 1px solid black; padding: 10px; text-align: center;}
                th {background-color: #4CAF50; color: white;}
            </style>
        </head>
        <body>
            <h2>Exam Marks Details</h2>
            <table>
                <tr>
                    <th>Exam List</th>
                    <th>Obtained Marks</th>
                    <th>Total Marks</th>
                </tr>
        """

        for exam, omark, tmark in zip(exams,marks,tmarks):
            html_table += f"<tr><td>{exam}</td><td>{omark}</td><td>{tmark}</td></tr>"

        html_table += """
            </table>
        </body>
        </html>
        """

        # Create Email
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "Exam Marks Report"

        # Attach HTML Content
        msg.attach(MIMEText(html_table, "html"))
        
        if st.button("Send Mail"):
            try:
                # Connect to SMTP Server and Send Email
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()  # Secure connection
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
                server.quit()
                st.success("Email sent successfully!")
            except Exception as e:
                st.write(f"Error sending email: {e}")