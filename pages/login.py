import streamlit as st
from .student import app as student
from .admin import app as admin
from queries.queries import verify_user

b1 = "notlogin"

def app():
    global b1
    cont = st.empty()
    with cont.container():
        b1 = "notlogin"
        st.title('Login')
        
        st.write("This is the About Us Page of the DBMS Project")

        st.write("Login To the best website")
        
        username = st.text_input("Username ")
        password = st.text_input("Password ", type="password")

        if(st.button("Login")):
            if(not verify_user(username, password)):
                st.error('incorrect password or username')
            else:
                b1 = "login"
    
    if b1 == "login":
        cont.empty()
        if username == "admin":
           admin(username, password)
        else:
            student(username, password)
        # signout = st.empty()
        # with signout.container():
        #     if(st.button("Sign out")):
        #         username = ""
        #         password = ""
        #         b1 = 'notlogin'
        # if b1 == 'notlogin':
        #     signout.empty()