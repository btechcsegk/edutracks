import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

    # Sample data: Creating a dataframe with student information
def StudentPage():
    data = {
    'Student ID': [101, 102, 103, 104, 105],
    'Name': ['John Doe', 'Jane Smith', 'Tom Brown', 'Emily Davis', 'Michael Lee'],
    'Age': [20, 22, 21, 23, 20],
    'Grade': ['A', 'B', 'A', 'C', 'B'],
    'Math': [95, 88, 92, 70, 85],
    'English': [90, 80, 85, 65, 75],
    'Science': [92, 85, 88, 72, 80],
    'History': [85, 78, 80, 60, 70],
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Title of the dashboard
    st.title("Student Dashboard")

    # Display basic student information
    st.header("Student Information")
    st.dataframe(df[['Student ID', 'Name', 'Age', 'Grade']])

    # Section for academic performance
    st.header("Academic Performance")

    # Add a selector to choose a student
    student_name = st.selectbox("Select Student", df['Name'])

    # Display student's scores in various subjects
    student_data = df[df['Name'] == student_name].iloc[0]
    st.subheader(f"{student_name}'s Scores")
    st.write(f"Math: {student_data['Math']}")
    st.write(f"English: {student_data['English']}")
    st.write(f"Science: {student_data['Science']}")
    st.write(f"History: {student_data['History']}")

    # Display a bar chart of the selected student's performance
    subjects = ['Math', 'English', 'Science', 'History']
    scores = [student_data['Math'], student_data['English'], student_data['Science'], student_data['History']]

    fig, ax = plt.subplots()
    ax.bar(subjects, scores, color='skyblue')
    ax.set_xlabel('Subjects')
    ax.set_ylabel('Scores')
    ax.set_title(f'{student_name} - Academic Performance')

    # Section for Grade Distribution
    st.header("Grade Distribution")

    # Plot grade distribution as a pie chart
    grade_counts = df['Grade'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(grade_counts)))
    ax2.set_title("Grade Distribution")

    # Section for Student Age Distribution
    st.header("Age Distribution of Students")
    fig3, ax3 = plt.subplots()
    sns.histplot(df['Age'], kde=True, ax=ax3, color='purple', bins=5)
    ax3.set_title('Age Distribution')

    # Display all three charts in a single row using st.columns()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.pyplot(fig)  # Bar chart
    with col2:
        st.pyplot(fig2)  # Pie chart
    with col3:
        st.pyplot(fig3)  # Histogram

    # Section for Student Statistics
    st.header("Student Statistics")
    st.write(f"Average Age of Students: {df['Age'].mean():.2f} years")
    st.write(f"Highest Score in Math: {df['Math'].max()} (Student: {df.loc[df['Math'].idxmax()]['Name']})")
    st.write(f"Lowest Score in Science: {df['Science'].min()} (Student: {df.loc[df['Science'].idxmin()]['Name']})")

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
    if st.button("Download Report"):
        pdf_buffer = generate_pdf(student_name, student_data, fig, fig2, fig3)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"{student_name}_report.pdf",
            mime="application/pdf"
        )