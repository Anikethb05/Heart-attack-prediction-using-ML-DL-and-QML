# Constants used in the Mediscope AI application

FEATURE_LISTS = {
    'heart-attack': [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ],
    'breast-cancer': [
        'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
        'smoothness_mean', 'compactness_mean', 'concavity_mean',
        'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
        'radius_se', 'texture_se', 'perimeter_se', 'area_se',
        'smoothness_se', 'compactness_se', 'concavity_se',
        'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
        'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
        'smoothness_worst', 'compactness_worst', 'concavity_worst',
        'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
    ],
    'diabetes': [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ],
    'lung-cancer': [
        'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
        'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY',
        'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING',
        'SHORTNESS_OF_BREATH', 'SWALLOWING_DIFFICULTY', 'CHEST_PAIN'
    ]
}

# Mapping of human-readable labels to numeric values
LABEL_TO_NUMERIC = {
    'heart-attack': {
        'sex': {'female': 0, 'male': 1},
        'cp': {'typical_angina': 0, 'atypical_angina': 1,
               'non_anginal_pain': 2, 'asymptomatic': 3},
        'fbs': {'false': 0, 'true': 1},
        'restecg': {'normal': 0, 'st_t_abnormality': 1, 'lv_hypertrophy': 2},
        'exang': {'no': 0, 'yes': 1},
        'slope': {'upsloping': 0, 'flat': 1, 'downsloping': 2},
        'ca': {'0': 0, '1': 1, '2': 2, '3': 3},
        'thal': {'normal': 0, 'fixed_defect': 1, 'reversible_defect': 2}
    },
    'lung-cancer': {
        'GENDER': {'F': 0, 'M': 1},
        'SMOKING': {'1': 0, '2': 1},
        'YELLOW_FINGERS': {'1': 0, '2': 1},
        'ANXIETY': {'1': 0, '2': 1},
        'PEER_PRESSURE': {'1': 0, '2': 1},
        'CHRONIC_DISEASE': {'1': 0, '2': 1},
        'FATIGUE': {'1': 0, '2': 1},
        'ALLERGY': {'1': 0, '2': 1},
        'WHEEZING': {'1': 0, '2': 1},
        'ALCOHOL_CONSUMING': {'1': 0, '2': 1},
        'COUGHING': {'1': 0, '2': 1},
        'SHORTNESS_OF_BREATH': {'1': 0, '2': 1},
        'SWALLOWING_DIFFICULTY': {'1': 0, '2': 1},
        'CHEST_PAIN': {'1': 0, '2': 1}
    }
}

MODEL_DISPLAY_NAMES = {
    "RF": "Random Forest",
    "KNN": "K-Nearest Neighbors",
    "DT": "Decision Tree",
    "LR": "Logistic Regression", 
    "SVM": "Support Vector Machine",
    "NB": "Naive Bayes",
    "DL": "Deep Learning"
}

FEATURE_DISPLAY_NAMES = {
    'heart-attack': {
        'age': "Age",
        'sex': "Sex",
        'cp': "Chest Pain Type",
        'trestbps': "Resting Blood Pressure",
        'chol': "Cholesterol",
        'fbs': "Fasting Blood Sugar",
        'restecg': "Resting ECG",
        'thalach': "Maximum Heart Rate",
        'exang': "Exercise Induced Angina",
        'oldpeak': "ST Depression",
        'slope': "Slope",
        'ca': "Number of Major Vessels",
        'thal': "Thalassemia"
    },
    'lung-cancer': {
        'AGE': "Age",
        'GENDER': "Gender",
        'SMOKING': "Smoking",
        'YELLOW_FINGERS': "Yellow Fingers",
        'ANXIETY': "Anxiety",
        'PEER_PRESSURE': "Peer Pressure",
        'CHRONIC_DISEASE': "Chronic Disease",
        'FATIGUE': "Fatigue",
        'ALLERGY': "Allergy",
        'WHEEZING': "Wheezing",
        'ALCOHOL_CONSUMING': "Alcohol Consuming",
        'COUGHING': "Coughing",
        'SHORTNESS_OF_BREATH': "Shortness of Breath",
        'SWALLOWING_DIFFICULTY': "Swallowing Difficulty",
        'CHEST_PAIN': "Chest Pain"
    }
}

OPTION_DISPLAY_NAMES = {
    'heart-attack': {
        'sex': {
            'female': "Female",
            'male': "Male"
        },
        'cp': {
            'typical_angina': "Typical Angina",
            'atypical_angina': "Atypical Angina",
            'non_anginal_pain': "Non-Anginal Pain",
            'asymptomatic': "Asymptomatic"
        },
        'fbs': {
            'false': "False (≤ 120 mg/dl)",
            'true': "True (> 120 mg/dl)"
        },
        'restecg': {
            'normal': "Normal",
            'st_t_abnormality': "ST-T Wave Abnormality",
            'lv_hypertrophy': "Probable/Definite LV Hypertrophy"
        },
        'exang': {
            'no': "No",
            'yes': "Yes"
        },
        'slope': {
            'upsloping': "Upsloping",
            'flat': "Flat",
            'downsloping': "Downsloping"
        },
        'thal': {
            'normal': "Normal",
            'fixed_defect': "Fixed Defect",
            'reversible_defect': "Reversible Defect",
            'other': "Other"
        }
    },
    'lung-cancer': {
        'GENDER': {
            'F': "Female",
            'M': "Male"
        },
        'binary_options': {
            '1': "No",
            '2': "Yes"
        }
    }
}