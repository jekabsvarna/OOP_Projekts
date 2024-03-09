# fetchLecturers.py

import sqlite3

def get_lecturers(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Query to select all users where role is 'lecturer'
    query = "SELECT id, email, first_name, role FROM user WHERE role='lecturer'"

    # Execute the query
    cur.execute(query)

    # Fetch all results
    lecturers = cur.fetchall()

    # Close the connection
    conn.close()

    return lecturers
