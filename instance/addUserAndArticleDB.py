import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

try:
    cur.execute('''
    CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        email VARCHAR(150) UNIQUE,
        password VARCHAR(150),
        first_name VARCHAR(150),
        role VARCHAR(10) DEFAULT 'student'
    );
    ''')
    print('Created Database!')
except sqlite3.OperationalError:
    print('Database already exists.')

try:
    cur.execute('''
    CREATE TABLE workshop (
        id INTEGER PRIMARY KEY,
        title VARCHAR(255),
        date DATETIME,
        lecturer_id INTEGER,
        FOREIGN KEY (lecturer_id) REFERENCES user (id)
    );
    ''')
    print('Created workshop table!')
except sqlite3.OperationalError as e:
    print(f'Error creating workshop table: {e}')

try:
    cur.execute('''
    CREATE TABLE enrollment (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        workshop_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES user (id),
        FOREIGN KEY (workshop_id) REFERENCES workshop (id)
    );
    ''')
    print('Created enrollment table!')
except sqlite3.OperationalError:
    print('Enrollment table already exists.')


admin_email = "admin@rtu.lv"
admin_password = "secureadminpassword"  
admin_first_name = "Admin"
admin_role = "admin"

try:
    cur.execute("INSERT INTO user (email, password, first_name, role) VALUES (?, ?, ?, ?)",
                (admin_email, admin_password, admin_first_name, admin_role))
    print(f"Added admin user: {admin_email}")
except sqlite3.IntegrityError as e:
    print(f"Error adding admin user: {e}")

lecturers = [
    ("Janis", "Berzins"),
    ("Peteris", "Ozolins"),
    ("Andris", "Kalnins"),
    ("Liene", "Liepina"),
    ("Anna", "Vitola"),
    ("Kristine", "Jansone"),
    ("Martins", "Krumins"),
    ("Ieva", "Ozola"),
    ("Zane", "Birzina"),
    ("Edgars", "Rozitis")
]

password = "securepassword"

for first_name, last_name in lecturers:
    email = f"{first_name.lower()}.{last_name.lower()}@rtu.lv"
    role = "lecturer"
    try:
        cur.execute("INSERT INTO user (email, password, first_name, role) VALUES (?, ?, ?, ?)",
                    (email, password, first_name + " " + last_name, role))
        print(f"Added {first_name} {last_name}")
    except sqlite3.IntegrityError as e:
        print(f"Error adding {first_name} {last_name}: {e}")

try:
    cur.execute('''
    CREATE TABLE article (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        student_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES user (id)
    );
    ''')
    print('Created article table!')
except sqlite3.OperationalError:
    print('Article table already exists.')

article_names = []

for name in article_names:
    try:
        cur.execute("INSERT INTO article (name) VALUES (?)", (name,))
        print(f"Added article: {name}")
    except sqlite3.IntegrityError as e:
        print(f"Error adding article: {e}")

conn.commit()
conn.close()

print("Finished setting up the database with an admin, lecturers, and articles.")
