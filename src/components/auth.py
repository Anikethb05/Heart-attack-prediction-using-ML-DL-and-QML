# File: /mediscope-ai/mediscope-ai/src/components/auth.py

import streamlit as st
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect('medical.db')

def show_login():
    st.title("HELLO DOC!")
    st.subheader("Login")
    
    init_db()
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        create_account = st.form_submit_button("Create Account")

        if submit_button:
            if not username or not password:
                st.error("Please enter both username and password")
                return

            with get_db() as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM doctors WHERE username=?", (username,))
                user = c.fetchone()
               
    
                if user and check_password_hash(user[2], password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.doctor_id = user[0]
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        if create_account:
            if not username or not password:
                st.error("Please enter both username and password")
                return
                
            conn = sqlite3.connect('medical.db')
            c = conn.cursor()
            try:
                hashed_password = generate_password_hash(password)
                c.execute("INSERT INTO doctors (username, password) VALUES (?, ?)",
                         (username, hashed_password))
                conn.commit()
                st.success("Account created successfully!")
            except sqlite3.IntegrityError:
                st.error("Username already exists")
            finally:
                conn.close()