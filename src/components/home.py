import streamlit as st
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from components.auth import init_db, get_db

def show_home():
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome to MediScope AI</h1>", unsafe_allow_html=True)
    
    st.write("""
    We offer an AI-powered medical diagnosis platform that assists healthcare 
    professionals in accurately and efficiently predicting diseases such as 
    heart disease, lung cancer, breast cancer, and diabetes. 
    
    Our system leverages 
    a diverse suite of machine learning and deep learning models — including K-Nearest 
    Neighbors, Support Vector Machines, Logistic Regression, Naive Bayes, Decision Trees, 
    Random Forests, and advanced neural networks. Additionally, we integrate cutting-edge 
    Quantum Machine Learning (QML) techniques to enhance diagnostic accuracy and support precision medicine.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar login functionality
    # st.sidebar.title("Navigation")
    if not st.session_state.authenticated:
        st.sidebar.title("Login")
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Login", 
                                                    use_container_width=True,
                                                    type="primary")
            with col2:
                create_account = st.form_submit_button("Create Account", 
                                                     use_container_width=True,
                                                     type="primary")

            if submit_button:
                if not username or not password:
                    st.sidebar.error("Please enter both username and password")
                    return

                with get_db() as conn:
                    c = conn.cursor()
                    c.execute("SELECT * FROM doctors WHERE username=?", (username,))
                    user = c.fetchone()
                    
                    if user and check_password_hash(user[2], password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.doctor_id = user[0]
                        st.sidebar.success("Logged in successfully!")
                        st.session_state.page = "Home"
                        st.rerun()
                    else:
                        st.sidebar.error("Invalid username or password")

            if create_account:
                if not username or not password:
                    st.sidebar.error("Please enter both username and password")
                    return
                    
                with get_db() as conn:
                    c = conn.cursor()
                    try:
                        hashed_password = generate_password_hash(password)
                        c.execute("INSERT INTO doctors (username, password) VALUES (?, ?)",
                                 (username, hashed_password))
                        conn.commit()
                        st.sidebar.success("Account created successfully!")
                    except sqlite3.IntegrityError:
                        st.sidebar.error("Username already exists")
    else:
        st.sidebar.subheader(f"Welcome, {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = "Home"
            st.rerun()

def show_authenticated_home():
    st.title(f"Welcome, {st.session_state.username}")
    
    st.write("""
    Our platform uses advanced machine learning models to predict the likelihood 
    of various diseases, assisting you in providing better patient care.
    """)
    
    st.subheader("Disease Prediction Tools:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🫀 Heart Attack Prediction", use_container_width=True, 
                     key="heart_btn", 
                     help="Predict heart attack risk based on patient data"):
            st.session_state.page = "Heart Attack"
            st.rerun()
            
            
        if st.button("🎗️ Breast Cancer Prediction", use_container_width=True,
                     key="breast_btn",
                     help="Analyze breast cancer risk factors"):
            st.session_state.page = "Breast Cancer"
            st.rerun()
            
            
    with col2:
        if st.button("🩺 Diabetes Prediction", use_container_width=True,
                     key="diabetes_btn",
                     help="Evaluate diabetes risk factors"):
            st.session_state.page = "Diabetes"
            st.rerun()
            
            
        if st.button("🫁 Lung Cancer Prediction", use_container_width=True,
                     key="lung_btn",
                     help="Assess lung cancer risk indicators"):
            st.session_state.page = "Lung Cancer"
            st.rerun()
            

    # Add some space and a divider
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    Select any tool above to start making predictions
    </div>
    """, unsafe_allow_html=True)