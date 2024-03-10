
import sqlite3

def get_articles(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Query to select all users where role is 'lecturer'
    query = "SELECT id, name FROM article"

    # Execute the query
    cur.execute(query)

    # Fetch all results
    articles = cur.fetchall()

    # Close the connection
    conn.close()

    return articles
