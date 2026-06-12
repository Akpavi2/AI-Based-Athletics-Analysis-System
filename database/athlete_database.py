# =====================================
# IMPORT LIBRARIES
# =====================================

import sqlite3


# =====================================
# CONNECT DATABASE
# =====================================

connection = sqlite3.connect(
    "database/athletics.db",
    check_same_thread=False
)

cursor = connection.cursor()


# =====================================
# CREATE ATHLETES TABLE
# =====================================



cursor.execute("""

CREATE TABLE IF NOT EXISTS athletes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    age INTEGER,

    gender TEXT,

    height REAL,

    weight REAL,

    sprint_time REAL,

    endurance REAL,

    vertical_jump REAL,

    specialization TEXT,

    achievements TEXT,

    injury_history TEXT,

    profile_photo TEXT

)

""")


# =====================================
# SAVE DATABASE
# =====================================

connection.commit()

print("Database Connected Successfully")

# =====================================
# SHOW ALL ATHLETES
# =====================================

cursor.execute(
    "SELECT * FROM athletes"
)

records = cursor.fetchall()

print("\n===== ATHLETE RECORDS =====")

for record in records:

    print(record)


# =====================================
# CREATE USERS TABLE
# =====================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    role TEXT

)

""")

connection.commit()

print("Users Table Ready")

