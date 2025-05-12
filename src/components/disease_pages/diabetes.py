import ast
import streamlit as st
import pandas as pd
from utils.constants import FEATURE_LISTS, MODEL_DISPLAY_NAMES
from utils.helpers import get_gemini_recommendations
from utils.database import search_patient, save_patient_prediction
from components.navigation import show_disease_navigation

def show_diabetes():
    st.title("Diabetes Prediction")
    
    if 'models' not in st.session_state or not st.session_state.models:
        st.error("Models not loaded. Please restart the application.")
        return
        
    if 'diabetes' not in st.session_state.models:
        st.error("Diabetes models not found.")
        return

    # Navigation sidebar
    show_disease_navigation("Diabetes")

    # Patient information
    col1, col2 = st.columns([3, 1], gap="small")
    with col1:
        name = st.text_input("Patient Name", label_visibility="collapsed", placeholder="Enter patient name")
    with col2:
        search = st.button("Search", use_container_width=True)

    # Handle search
    if search and name:
        patient_data = search_patient(name, 'diabetes')
        if patient_data:
            st.success(f"Found previous record for {name}")
            # Parse stored features
            stored_features = ast.literal_eval(patient_data[2])
            st.session_state.stored_features = stored_features
            st.session_state.previous_prediction = patient_data[3]
        else:
            st.warning("No previous records found")
            if 'stored_features' in st.session_state:
                del st.session_state.stored_features
    
    # Model selection
    model_options = {k: MODEL_DISPLAY_NAMES[k] for k in ["RF", "KNN", "DT", "LR", "SVM", "NB", "DL"]}
    model_type = st.selectbox(
        "Select Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        placeholder="Select a model"
    )
    

    # Features input
    features = {}
    for feature in FEATURE_LISTS['diabetes']:
        default_value = (
            float(st.session_state.stored_features[feature]) 
            if hasattr(st.session_state, 'stored_features') 
            else 0.0
        )

        features[feature] = st.number_input(
            feature,
            value=default_value,
            help=f"Enter the value for {feature.lower()}"
        )
    
    if st.button("Predict"):
        if not name:
            st.warning("Please enter a patient name to save the prediction.")
            return
        try:
            # Prepare features
            feature_values = list(features.values())
            
            # Scale features
            scaled_features = st.session_state.models['diabetes']['scaler'].transform([feature_values])
            
            # Make prediction
            prediction = st.session_state.models['diabetes'][model_type].predict(scaled_features)[0]
            if name:  # Only save if a patient name was provided
                save_patient_prediction(name, 'diabetes', features, prediction)        


            # Show results
            if prediction >= 0.5:
                st.error("High Risk of Diabetes")
                recommendations = get_gemini_recommendations('diabetes', {'age': features['Age']})
                st.subheader("Recommendations:")
                for rec in recommendations:
                    st.write("• " + rec)
            else:
                st.success("Low Risk of Diabetes")
                
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")