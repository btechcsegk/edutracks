import streamlit as st
from datasource import remoteDataSource

def HomePage():
    with open("assets/home_page.css") as f:
        st.html(f"<style>{f.read()}</style>")
    
    col1,col2 = st.columns([1,1])
    with col2:
        con = st.container(key="login-container")
        con.image("assets/text_signin.svg",width=100)
        con.write("***An interactive system for tracking student attendance and performance.***")
        
        con.markdown("__Enter Username__")
        user_field = con.container(key="user-field")
        con.markdown("__Enter Password__")
        passwd_field = con.container(key="passwd-field")
        # user_field.image("assets/user.svg",width=28)
        username = user_field.text_input("__Enter UserId__", placeholder="2204921540060",label_visibility="collapsed")
        # col_passwd_img.image("assets/lock.svg",width=28)
        password = passwd_field.text_input("__Enter Your Password__", placeholder="password", type="password",label_visibility="collapsed")
        
        def HandleLogin():
            res = remoteDataSource.loginByRole(username,password)
            if res != "False":
                st.session_state.page = res['role']
                st.session_state.uid = res['username']
                st.session_state.name = res['name']
            else:
                con.error("Userid or password is inavlid!")
                
            
        con.button("Login",on_click=HandleLogin,key="btn-login")
            
            
    with col1:
        img_con = st.container(key="main-img-container")
        img_con.image("assets/side_img.png")
        