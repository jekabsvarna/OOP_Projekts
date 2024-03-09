# fetchStudents.py

import sqlite3

def get_students(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Query to select all users where role is 'student'
    query = "SELECT id, email, first_name, role FROM user WHERE role='student'"

    # Execute the query
    cur.execute(query)

    # Fetch all results
    students = cur.fetchall()

    # Close the connection
    conn.close()

    return students
