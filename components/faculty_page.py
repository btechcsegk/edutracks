import streamlit as st
import pandas as pd

# Sample Faculty Data
def FacultyPage():
    data = {
        'Faculty ID': [1, 2, 3],
        'Name': ['Dr. John Doe', 'Prof. Jane Smith', 'Dr. Emily Davis'],
        'Department': ['Computer Science', 'Mathematics', 'Physics'],
        'Email': ['john.doe@example.com', 'jane.smith@example.com', 'emily.davis@example.com']
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Title of the Dashboard
    st.title("Faculty Admin Panel")

    # Sidebar Navigation
    sidebar_options = ['View Faculty', 'Add Faculty', 'Update Faculty', 'Delete Faculty']
    selection = st.sidebar.radio("Select Option", sidebar_options)

    # View Faculty Section
    if selection == 'View Faculty':
        st.header("Faculty List")
        st.dataframe(df)

    # Add New Faculty Section
    elif selection == 'Add Faculty':
        st.header("Add New Faculty")
        
        with st.form(key='faculty_form'):
            name = st.text_input("Name")
            department = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics", "Biology", "Chemistry"])
            email = st.text_input("Email")
            
            submit_button = st.form_submit_button(label='Add Faculty')

        if submit_button:
            # Create a new faculty entry
            new_id = df['Faculty ID'].max() + 1  # Generate new ID
            new_faculty = pd.DataFrame({
                'Faculty ID': [new_id],
                'Name': [name],
                'Department': [department],
                'Email': [email]
            })
            
            # Append the new faculty to the existing data
            df = pd.concat([df, new_faculty], ignore_index=True)
            st.success(f"New faculty {name} added successfully!")
            st.dataframe(df)

    # Update Faculty Section
    elif selection == 'Update Faculty':
        st.header("Update Faculty Information")
        
        faculty_id = st.selectbox("Select Faculty to Update", df['Faculty ID'])
        selected_faculty = df[df['Faculty ID'] == faculty_id].iloc[0]
        
        with st.form(key='update_form'):
            name = st.text_input("Name", value=selected_faculty['Name'])
            department = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics", "Biology", "Chemistry"], index=["Computer Science", "Mathematics", "Physics", "Biology", "Chemistry"].index(selected_faculty['Department']))
            email = st.text_input("Email", value=selected_faculty['Email'])
            
            submit_button = st.form_submit_button(label='Update Faculty')
        
        if submit_button:
            # Update the faculty data
            df.loc[df['Faculty ID'] == faculty_id, 'Name'] = name
            df.loc[df['Faculty ID'] == faculty_id, 'Department'] = department
            df.loc[df['Faculty ID'] == faculty_id, 'Email'] = email
            
            st.success(f"Faculty {name} updated successfully!")
            st.dataframe(df)

    # Delete Faculty Section
    elif selection == 'Delete Faculty':
        st.header("Delete Faculty")
        
        faculty_id = st.selectbox("Select Faculty to Delete", df['Faculty ID'])
        selected_faculty = df[df['Faculty ID'] == faculty_id].iloc[0]
        
        delete_button = st.button(f"Delete {selected_faculty['Name']}")
        
        if delete_button:
            # Delete the selected faculty
            df = df[df['Faculty ID'] != faculty_id]
            st.success(f"Faculty {selected_faculty['Name']} deleted successfully!")
            st.dataframe(df)
