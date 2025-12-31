
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="hospital.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Patients Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                medical_history TEXT,
                status TEXT
            )
        ''')

        # Doctors Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                specialty TEXT,
                bio TEXT,
                contact TEXT
            )
        ''')

        # Operations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                op_type TEXT,
                op_date TEXT,
                status TEXT, -- 'Done', 'Pending'
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id)
            )
        ''')

        conn.commit()
        
        # Seed Data if empty
        cursor.execute('SELECT count(*) FROM doctors')
        if cursor.fetchone()[0] == 0:
            self.seed_data(cursor)
            conn.commit()
            
        conn.close()

    def seed_data(self, cursor):
        # Seed Doctor
        bio = ("Senior Biomedical Engineer & Chief Surgeon. "
               "Expert in robotic surgery and AI-driven diagnostics.")
        cursor.execute('''
            INSERT INTO doctors (full_name, specialty, bio, contact)
            VALUES (?, ?, ?, ?)
        ''', ("Youssef BEN LETAIFA", "Neurosurgeon / Biomedical Expert", bio, "+1 234 567 890"))
        
        doc_id = cursor.lastrowid

        # Seed Patient
        history = (
            "Medical History:\n"
            "- Hypertension (Diagnosed 2015)\n"
            "- Type 2 Diabetes (Managed via Metformin)\n"
            "- Psoriasis (Mild)\n\n"
            "Surgical History:\n"
            "- Appendectomy (Laproscopic, 2018)\n"
            "- Tonsillectomy (Childhood)\n\n"
            "Allergies:\n"
            "- Peanuts (Severe)\n"
            "- Penicillin (Rash)\n\n"
            "Current Medications:\n"
            "- Lisinopril 10mg daily\n"
            "- Metformin 500mg bid"
        )
        cursor.execute('''
            INSERT INTO patients (full_name, age, gender, medical_history, status)
            VALUES (?, ?, ?, ?, ?)
        ''', ("el Touhami", 54, "Male", history, "Pre-Op Preparation"))

        
        pat_id = cursor.lastrowid
        
        # Seed Operations
        ops = [
            (pat_id, doc_id, "Craniotomy", "2024-12-20", "Pending"),
            (pat_id, doc_id, "Routine Checkup", "2024-11-15", "Done")
        ]
        cursor.executemany('''
            INSERT INTO operations (patient_id, doctor_id, op_type, op_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', ops)
        
        print("Database seeded successfully.")

    def get_doctor(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM doctors LIMIT 1')
        res = c.fetchone()
        conn.close()
        return res

    def get_patients(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT id, full_name FROM patients')
        res = c.fetchall()
        conn.close()
        return res

    def get_patient_details(self, pat_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM patients WHERE id = ?', (pat_id,))
        res = c.fetchone()
        conn.close()
        return res

    def get_operations(self, doctor_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            SELECT operations.op_date, operations.op_type, patients.full_name, operations.status 
            FROM operations 
            JOIN patients ON operations.patient_id = patients.id
            WHERE doctor_id = ?
        ''', (doctor_id,))
        res = c.fetchall()
        conn.close()
        return res

    def add_patient(self, name, age, history):
         conn = self.get_connection()
         c = conn.cursor()
         c.execute('INSERT INTO patients (full_name, age, gender, medical_history, status) VALUES (?, ?, ?, ?, ?)',
                   (name, age, "Unknown", history, "Pending Assessment"))
         conn.commit()
         conn.close()

