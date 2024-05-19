
import sqlite3

def get_articles(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = "SELECT id, name FROM article"

    cur.execute(query)

    articles = cur.fetchall()

    conn.close()

    return articles
