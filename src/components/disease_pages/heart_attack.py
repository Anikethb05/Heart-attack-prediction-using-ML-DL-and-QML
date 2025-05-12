import ast
import streamlit as st
import pandas as pd
import numpy as np
from utils.constants import FEATURE_LISTS, LABEL_TO_NUMERIC, MODEL_DISPLAY_NAMES, FEATURE_DISPLAY_NAMES, OPTION_DISPLAY_NAMES
from utils.helpers import get_gemini_recommendations
from utils.database import search_patient, save_patient_prediction
from components.navigation import show_disease_navigation

def show_heart_attack():
    st.title("Heart Attack Prediction")
    
    if 'models' not in st.session_state or not st.session_state.models:
        st.error("Models not loaded. Please restart the application.")
        return
        
    if 'heart-attack' not in st.session_state.models:
        st.error("Heart attack models not found.")
        return

    # Navigation sidebar
    show_disease_navigation("Heart Attack")

    # Patient information
    col1, col2 = st.columns([3, 1], gap="small")
    with col1:
        name = st.text_input("Patient Name", label_visibility="collapsed", placeholder="Enter patient name")
    with col2:
        search = st.button("Search", use_container_width=True)


    # Handle search
    if search and name:
        patient_data = search_patient(name, 'heart_attack')
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
        format_func=lambda x: model_options[x]
    )

    # Features input with proper display names
    features = {}
    display_names = FEATURE_DISPLAY_NAMES['heart-attack']
    options = OPTION_DISPLAY_NAMES['heart-attack']
    
    for feature in FEATURE_LISTS['heart-attack']:
        if feature in LABEL_TO_NUMERIC['heart-attack']:
            stored_value = (
                st.session_state.stored_features.get(feature, 
                    list(LABEL_TO_NUMERIC['heart-attack'][feature].keys())[0]
                ) if hasattr(st.session_state, 'stored_features') 
                else list(LABEL_TO_NUMERIC['heart-attack'][feature].keys())[0]
            )
            features[feature] = st.selectbox(
                display_names[feature],
                options=list(LABEL_TO_NUMERIC['heart-attack'][feature].keys()),
                index=list(LABEL_TO_NUMERIC['heart-attack'][feature].keys()).index(stored_value),
                format_func=lambda x, f=feature: options[f][x] if f in options else x
            )
        else:
            default_value = (
                float(st.session_state.stored_features.get(feature, 0.0)
                ) if hasattr(st.session_state, 'stored_features') 
                else 0.0
            )
            features[feature] = st.number_input(display_names[feature], value=default_value)
        
    if st.button("Predict"):
        if not name:
            st.warning("Please enter a patient name to save the prediction.")
            return
        try:
            # Convert categorical features to numeric
            numeric_features = []
            for feature, value in features.items():
                if feature in LABEL_TO_NUMERIC['heart-attack']:
                    numeric_value = LABEL_TO_NUMERIC['heart-attack'][feature][value]
                else:
                    numeric_value = float(value)
                numeric_features.append(numeric_value)
            
            # Scale features
            scaled_features = st.session_state.models['heart-attack']['scaler'].transform([numeric_features])
            
            # Make prediction
            prediction = st.session_state.models['heart-attack'][model_type].predict(scaled_features)[0]
            if name:  # Only save if a patient name was provided
                save_patient_prediction(name, 'heart_attack', features, prediction)

            # Show results
            if prediction >= 0.5:
                st.error("High Risk of Heart Attack")
                age_value = features.get('age', features.get('Age', 0))  # Try both cases
                recommendations = get_gemini_recommendations('heart-attack', {'age': age_value})
                st.subheader("Recommendations:")
                for rec in recommendations:
                    st.write("• " + rec)
            else:
                st.success("Low Risk of Heart Attack")
                
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")