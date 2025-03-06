# Setup AgGrid options
        # gb = GridOptionsBuilder.from_dataframe(df)
        # gb.configure_selection('single')  # Allow single row selection
        # grid_options = gb.build()

        # # Display AgGrid interactive table
        # response = AgGrid(df, gridOptions=grid_options)
        
        # def deleteFaculty(email):
        #     db.delete_faculty(email)
        # Get selected row data
        # selected_row = response.get('selected_rows', [])
        # if isinstance(selected_row,pd.DataFrame):
        #     name = list(selected_row['Name'])
        #     email = list(selected_row['Email'])
        #     cols = st.columns(4)
        #     cols[0].write(name[0])
        #     cols[1].write(email[0])
        #     cols[2].button("Update", key="update-faculty")
        #     if cols[3].button("Delete", key="delete-faculty"):
        #         deleteFaculty(email[0])

    # Add New Faculty Section