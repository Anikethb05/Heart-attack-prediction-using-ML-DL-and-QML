import sqlite3
from pathlib import Path

def get_db_connection():
    db_path = Path(__file__).parent.parent.parent / 'database' / 'patients.db'
    return sqlite3.connect(db_path)

def search_patient(name, disease_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            f"SELECT * FROM {disease_type}_predictions WHERE patient_name = ? ORDER BY prediction_date DESC LIMIT 1", 
            (name,)
        )
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error searching patient: {e}")
        return None
    finally:
        conn.close()

def save_patient_prediction(name, disease_type, features, prediction):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Convert features dict to string representation
        features_str = str(features)
        
        cursor.execute(
            f"""
            INSERT INTO {disease_type}_predictions 
            (patient_name, features, prediction, prediction_date) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (name, features_str, prediction)
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving prediction: {e}")
    finally:
        conn.close()