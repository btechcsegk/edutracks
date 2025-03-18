import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import db

def getFetchOne(val):
    if val is not None:
        return val[0] 

def StudentPage():
    
    sub_count = getFetchOne(db.get_subject_count(2204921540059))
    att = db.get_average_attendance_by_id(st.session_state.uid)
    sem = getFetchOne(db.get_semester_by_id(st.session_state.uid))
    
    
    name_con = st.container(key="name-con")
    name_con.write(f"🚀 {st.session_state.name}'s Dashboard 🚀")
    
    with open("assets/student_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    
    st.header("Overview")
    mcol1,mcol2,mcol3 = st.columns(3,gap="medium")
    
    with mcol1:
        mcon = st.container(key="m-sub")
        mcon.image("assets/sub.png", width=100)
        mcon.markdown(f"### Subject Count\n##### __:rainbow[{sub_count}]__")
    with mcol2:
        mcon = st.container(key="m-att")
        mcon.image("assets/att.png", width=100)
        mcon.markdown(f"### My Attendance\n##### __:rainbow[{round(att[0]/att[1]*100,2) if att is not None else 0}]__%")
    with mcol3:
        mcon = st.container(key="m-sem")
        mcon.image("assets/sem.png", width=100)
        mcon.markdown(f"### Current Semester\n##### __:rainbow[{sem}]__")
    
    
    mcol4, mcol5 = st.columns([2,1],gap="medium")
    with mcol4:   
        st.header("Results Analysis")
        res_con = st.container(key="res-con")
        mark_data =db.get_marks_subject_wise(st.session_state.uid) if db.get_marks_subject_wise(st.session_state.uid) is not None else []
        
        exams = [i[0] for i in mark_data if len(mark_data)!=0]
        obt_marks = [i[1] for i in mark_data if len(mark_data)!=0]
        tot_marks = [i[2] for i in mark_data if len(mark_data)!=0]
        
        
        # Matplotlib Bar Chart 
        if len(exams)>0:
            df = pd.DataFrame({'Exams':exams,'Total Marks':tot_marks,'Obtained Marks':obt_marks})
            col_list=list(df.columns)
            fig = df.plot(kind='bar',x=col_list[0],y=col_list[1:])
            plt.xticks(rotation=20)
            with res_con.columns([1,6,1])[1]:
                st.pyplot(fig.figure)
        else:
            st.write("No Results Found")
        
        
    with mcol5:   
        st.header("Subject-Wise Attendance")
        att_con = st.container(key="att-con")
        
        att_list = db.get_att_by_s_id_and_sem(st.session_state.uid)
        
        if att_list is not None:
            for i in att_list:
                progress_style = f"""
                <label for="file" style="font-family: Arial, sans-serif; font-size: 16px; color: #333; margin-bottom: 8px; display: block;">{i[0]}</label>
                <progress id="file" value="{i[1]}" max="{i[2]}" style="width: 80%; height: 20px; background-color:#f2f2f2; border-radius: 10px;">
                    <div style="color: #333; font-size: 14px; display:flex; width:80%; justify-content:space-between; line-height: 25px;"><p>__{i[1]}__</p><p>__{i[2]}__</p></div>
                </progress>
                """
                att_con.markdown(progress_style, unsafe_allow_html=True)
        else:
            att_con.write("No attendance Found")
        
        
        
        
    # Function to generate the PDF report
    def generate_pdf(student_name, student_data, fig, fig2, fig3):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Title
        c.setFont("Helvetica", 16)
        c.drawString(100, 750, f"Student Report: {student_name}")
        
        # Basic Info
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, f"Student ID: {student_data['Student ID']}")
        c.drawString(100, 700, f"Age: {student_data['Age']}")
        c.drawString(100, 680, f"Grade: {student_data['Grade']}")
        
        # Academic Performance
        c.drawString(100, 650, "Academic Performance:")
        c.drawString(100, 630, f"Math: {student_data['Math']}")
        c.drawString(100, 610, f"English: {student_data['English']}")
        c.drawString(100, 590, f"Science: {student_data['Science']}")
        c.drawString(100, 570, f"History: {student_data['History']}")
        
        # Save the PDF
        c.showPage()
        
        # Save plots to buffer (PNG images)
        fig.savefig("temp_chart.png")
        fig2.savefig("temp_pie.png")
        fig3.savefig("temp_histogram.png")
        
        # Attach images to PDF
        c.drawImage("temp_chart.png", 100, 400, width=400, height=250)
        c.drawImage("temp_pie.png", 100, 150, width=400, height=250)
        c.drawImage("temp_histogram.png", 100, -100, width=400, height=250)
        
        c.save()
        
        buffer.seek(0)
        return buffer

    # Allow user to download the report
    # if st.button("Download Report"):
    #     pdf_buffer = generate_pdf(student_name, student_data, fig, fig2, fig3)
    #     st.download_button(
    #         label="Download PDF Report",
    #         data=pdf_buffer,
    #         file_name=f"{student_name}_report.pdf",
    #         mime="application/pdf"
    #     )