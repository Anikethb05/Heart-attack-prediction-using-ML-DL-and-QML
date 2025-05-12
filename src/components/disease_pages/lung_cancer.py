import ast
import streamlit as st
import pandas as pd
from utils.constants import FEATURE_LISTS, LABEL_TO_NUMERIC, MODEL_DISPLAY_NAMES, FEATURE_DISPLAY_NAMES, OPTION_DISPLAY_NAMES
from utils.helpers import get_gemini_recommendations
from utils.database import search_patient, save_patient_prediction
from components.navigation import show_disease_navigation

def show_lung_cancer():
    st.title("Lung Cancer Prediction")
    
    if 'models' not in st.session_state or not st.session_state.models:
        st.error("Models not loaded. Please restart the application.")
        return
        
    if 'lung-cancer' not in st.session_state.models:
        st.error("Lung cancer models not found.")
        return

    # Navigation sidebar
    show_disease_navigation("Lung Cancer")

    # Patient information
    col1, col2 = st.columns([3, 1], gap="small")
    with col1:
        name = st.text_input("Patient Name", label_visibility="collapsed", placeholder="Enter patient name")
    with col2:
        search = st.button("Search", use_container_width=True)

    # Handle search
    if search and name:
        patient_data = search_patient(name, 'lung_cancer')
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
    
        # Features input
    features = {}
    display_names = FEATURE_DISPLAY_NAMES['lung-cancer']
    options = OPTION_DISPLAY_NAMES['lung-cancer']
    
    for feature in FEATURE_LISTS['lung-cancer']:
        if feature in LABEL_TO_NUMERIC['lung-cancer']:
            stored_value = (
                st.session_state.stored_features.get(feature, 'F' if feature == 'GENDER' else '1')
                if hasattr(st.session_state, 'stored_features') 
                else ('F' if feature == 'GENDER' else '1')
            )
            
            if feature == 'GENDER':
                feature_options = list(options['GENDER'].keys())
                display_func = lambda x, f=feature: options['GENDER'][x]
            else:
                feature_options = ['1', '2']
                display_func = lambda x: options['binary_options'][x]
                
            features[feature] = st.selectbox(
                display_names[feature],
                options=feature_options,
                index=feature_options.index(stored_value),
                format_func=display_func
            )
        else:
            default_value = (
                float(st.session_state.stored_features.get(feature, 0.0)) 
                if hasattr(st.session_state, 'stored_features') 
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
                if feature in LABEL_TO_NUMERIC['lung-cancer']:
                    numeric_value = LABEL_TO_NUMERIC['lung-cancer'][feature][value]
                else:
                    numeric_value = float(value)
                numeric_features.append(numeric_value)
            
            # Scale features
            scaled_features = st.session_state.models['lung-cancer']['scaler'].transform([numeric_features])
            
            # Make prediction
            prediction = st.session_state.models['lung-cancer'][model_type].predict(scaled_features)[0]
            
            if name:  # Only save if a patient name was provided
                save_patient_prediction(name, 'lung_cancer', features, prediction)


            # Show results
            if prediction >= 0.5:
                st.error("High Risk of Lung Cancer")
                recommendations = get_gemini_recommendations('lung-cancer', {'age': features['AGE']})
                st.subheader("Recommendations:")
                for rec in recommendations:
                    st.write("• " + rec)
            else:
                st.success("Low Risk of Lung Cancer")
                
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")