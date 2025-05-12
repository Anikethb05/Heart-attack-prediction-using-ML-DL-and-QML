import sqlite3
from pathlib import Path

def init_database():
    db_path = Path(__file__).parent.parent.parent / 'database' / 'patients.db'
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables for each disease type
    tables = [
        'heart_attack_predictions',
        'breast_cancer_predictions',
        'diabetes_predictions',
        'lung_cancer_predictions'
    ]

    for table in tables:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            features TEXT NOT NULL,
            prediction REAL NOT NULL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()