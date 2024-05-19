import sqlite3

def get_lecturers(db_path, limit=10, offset=0):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "SELECT id, email, first_name, role FROM user WHERE role='lecturer' LIMIT ? OFFSET ?"

    cur.execute(query, (limit, offset))

    lecturers = cur.fetchall()

    conn.close()

    return lecturers



def get_total_lecturers_count(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM user WHERE role='lecturer'"  

    cur.execute(query)

    count = cur.fetchone()[0]

    conn.close()

    return count