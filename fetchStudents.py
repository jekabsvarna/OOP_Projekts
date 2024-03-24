# fetchStudents.py

import sqlite3

def get_students(db_path, limit=10, offset=0):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Query to select all users where role is 'lecturer' with pagination
    # SQL parameters are passed in a tuple following the SQL query
    query = "SELECT id, email, first_name, role FROM user WHERE role='student' LIMIT ? OFFSET ?"

    # Execute the query with limit and offset parameters
    cur.execute(query, (limit, offset))

    # Fetch all results within the limit and offset
    students = cur.fetchall()

    # Close the connection
    conn.close()

    return students

def get_total_students_count(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Query to count all lecturers 
    query = "SELECT COUNT(*) FROM user WHERE role='student'"  

    # Execute the query
    cur.execute(query)

    # Fetch one result
    count = cur.fetchone()[0]
    #count = cur.fetchall()

    # Close the connection
    conn.close()

    return count