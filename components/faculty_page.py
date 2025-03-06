import streamlit as st
import pandas as pd

# Sample Faculty Data
def FacultyPage():
    main_col1,main_col2 = st.columns([3,2])
    
    with main_col1:
        col1,col2= st.columns(2)
        with col1:
            course_list = ["Select Course","BTech", "BCA"]
            course = st.selectbox("",course_list, label_visibility="collapsed")
            sem_list = ["Select Semester","Sem 1", "Sem 2", "Sem 3", "Sem 4",
                        "Sem 5","Sem 6","Sem 7","Sem 8"]
            if course=="BCA":
                sem_list = ["Select Semester","Sem 1", "Sem 2", "Sem 3", "Sem 4",
                        "Sem 5","Sem 6"]
            
            sem = st.selectbox("",sem_list, label_visibility="collapsed")
        
        with col2:
            con = st.container(key="stu-con")
            con.image("assets/reading_girl.png",width=100)
            con.markdown(f"### 2000 \n Student count")