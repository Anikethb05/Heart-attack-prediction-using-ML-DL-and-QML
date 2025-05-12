import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
import re

from components.home import show_home, show_authenticated_home
from components.auth import show_login
from components.disease_pages.heart_attack import show_heart_attack
from components.disease_pages.breast_cancer import show_breast_cancer
from components.disease_pages.diabetes import show_diabetes
from components.disease_pages.lung_cancer import show_lung_cancer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()

# Initialize GEMINI API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
    logger.info("Gemini API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini API: {str(e)}")

# Load models and scalers
def load_models():
    try:
        base_path = Path(__file__).parent / 'models'
        if not base_path.exists():
            logger.error(f"Models directory not found at {base_path}")
            return None
            
        models = {}
        diseases = ['heart-attack', 'breast-cancer', 'diabetes', 'lung-cancer']
        model_types = ['RF', 'KNN', 'DT', 'LR', 'SVM', 'NB', 'DL']
        
        for disease in diseases:
            models[disease] = {}
            disease_path = base_path / disease
            
            if not disease_path.exists():
                logger.warning(f"Disease directory not found: {disease_path}")
                continue
                
            try:
                # Load models without .pkl extension since your models don't have it
                for model_type in model_types:
                    model_path = disease_path / f'{model_type}_model'
                    if model_path.exists():
                        with open(model_path, 'rb') as f:
                            models[disease][model_type] = pickle.load(f)
                    else:
                        logger.warning(f"{model_type} model not found for {disease}")
                
                # Load scaler if it exists
                scaler_path = disease_path / 'scaler'
                if scaler_path.exists():
                    with open(scaler_path, 'rb') as f:
                        models[disease]['scaler'] = pickle.load(f)
                        
            except Exception as e:
                logger.error(f"Error loading models for {disease}: {str(e)}")
                continue
                
        return models
    except Exception as e:
        logger.error(f"Error in load_models: {str(e)}")
        return None

# Initialize session state
def init_session_state():
    if 'models' not in st.session_state:
        models = load_models()
        if not models:
            st.error("Failed to load models. Please check the logs and restart the application.")
        st.session_state.models = models
        
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    if 'username' not in st.session_state:
        st.session_state.username = None
        
    if 'doctor_id' not in st.session_state:
        st.session_state.doctor_id = None

    if 'page' not in st.session_state:
        st.session_state.page = "Home"


def main():
    st.set_page_config(page_title="MediScope AI", layout="wide")
    
    init_session_state()
    
    # Handle authentication
    if not st.session_state.authenticated:
        if st.session_state.page == "Login":
            show_login_page()
        else:
            show_home()
        return
        
    # Navigation sidebar
    st.sidebar.title("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = "Home"
        st.rerun()
    
    # Page routing
    if st.session_state.page == "Home":
        show_authenticated_home()
    elif st.session_state.page == "Heart Attack":
        show_heart_attack()
    elif st.session_state.page == "Breast Cancer":
        show_breast_cancer()
    elif st.session_state.page == "Diabetes":
        show_diabetes()
    elif st.session_state.page == "Lung Cancer":
        show_lung_cancer()

if __name__ == "__main__":
    main()