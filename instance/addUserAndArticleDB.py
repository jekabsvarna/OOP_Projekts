import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Create the user table
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

# Create the workshop table
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

# Create the enrollment table
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


# Admin user details
admin_email = "admin@rtu.lv"
admin_password = "secureadminpassword"  # Replace with a hashed password
admin_first_name = "Admin"
admin_role = "admin"

# Add the admin user to the database
try:
    cur.execute("INSERT INTO user (email, password, first_name, role) VALUES (?, ?, ?, ?)",
                (admin_email, admin_password, admin_first_name, admin_role))
    print(f"Added admin user: {admin_email}")
except sqlite3.IntegrityError as e:
    print(f"Error adding admin user: {e}")

# List of lecturer names (First name, Last name)
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

# Password for lecturers, for demonstration purposes. In a real application, ensure this is securely hashed.
password = "securepassword"

# Iterate over the lecturers list and insert each into the database
for first_name, last_name in lecturers:
    email = f"{first_name.lower()}.{last_name.lower()}@rtu.lv"
    role = "lecturer"
    try:
        cur.execute("INSERT INTO user (email, password, first_name, role) VALUES (?, ?, ?, ?)",
                    (email, password, first_name + " " + last_name, role))
        print(f"Added {first_name} {last_name}")
    except sqlite3.IntegrityError as e:
        print(f"Error adding {first_name} {last_name}: {e}")

# Create the article table
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

# List of article names
article_names = []

# Insert article names into the database
for name in article_names:
    try:
        cur.execute("INSERT INTO article (name) VALUES (?)", (name,))
        print(f"Added article: {name}")
    except sqlite3.IntegrityError as e:
        print(f"Error adding article: {e}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Finished setting up the database with an admin, lecturers, and articles.")
