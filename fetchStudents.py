import sqlite3

def get_students(db_path, limit=10, offset=0):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "SELECT id, email, first_name, role FROM user WHERE role='student' LIMIT ? OFFSET ?"

    cur.execute(query, (limit, offset))

    students = cur.fetchall()

    conn.close()

    return students

def get_total_students_count(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM user WHERE role='student'"  

    cur.execute(query)

    count = cur.fetchone()[0]

    conn.close()

    return count