import numpy as np
import pandas as pd
import google.generativeai as genai
import logging
from typing import List, Dict, Any
from utils.constants import LABEL_TO_NUMERIC

def get_gemini_recommendations(disease: str, patient_data: Dict[str, Any]) -> List[str]:
    """Get AI-generated recommendations for patient care."""
    try:
        prompt = f"""
        The patient has tested positive for {disease.replace('-', ' ')}.
        Patient details: Age: {patient_data.get('age', 'unknown')}.
        Provide exactly 5 concise, actionable recommendations for managing or treating this condition.
        Each recommendation should be a single sentence.
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise ValueError("Empty response from Gemini API")
            
        recommendations = response.text.split('\n')[:5]
        recommendations = [r.strip() for r in recommendations if r.strip()]
        
        return recommendations[:5] if recommendations else ["No recommendations available."]
        
    except Exception as e:
        logging.error(f"Gemini API error: {str(e)}")
        return ["Unable to retrieve recommendations at this time."]

def preprocess_data(input_data: Dict[str, Any], disease: str) -> List[float]:
    """Preprocess input data for model prediction."""
    numeric_features = []
    for feature, value in input_data.items():
        if feature in LABEL_TO_NUMERIC.get(disease, {}):
            numeric_value = LABEL_TO_NUMERIC[disease][feature].get(value)
            if numeric_value is None:
                raise ValueError(f"Invalid value for {feature}")
        else:
            try:
                numeric_value = float(value)
            except ValueError:
                raise ValueError(f"Invalid value for {feature}")
        numeric_features.append(numeric_value)
    return numeric_features

def classify_risk(prediction: float) -> str:
    """Classify risk level based on prediction value."""
    if prediction >= 0.8:
        return "High Risk"
    elif prediction >= 0.5:
        return "Medium Risk"
    return "Low Risk"

def format_patient_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Format patient record for display."""
    return {
        'name': record['name'],
        'age': record['age'],
        'prediction': f"{record['result']:.2%}",
        'risk_level': record['risk_label'],
        'date': record['date'].strftime('%Y-%m-%d %H:%M:%S')
    }
