import streamlit as st

def show_disease_navigation(current_page=None):
    """Display navigation buttons for disease pages"""  
    
    diseases = {
        "Heart Attack": "🫀",
        "Breast Cancer": "🎗️",
        "Diabetes": "🩺",
        "Lung Cancer": "🫁"
    }
    
    for disease, emoji in diseases.items():
        if disease != current_page:  # Don't show button for current page
            if st.sidebar.button(f"{emoji} {disease}", use_container_width=True):
                st.session_state.page = disease
                st.rerun()
       