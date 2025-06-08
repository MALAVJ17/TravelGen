import sqlite3

DB_NAME = "travel_itineraries.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)
    # Create itineraries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itineraries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        location TEXT,
        start_date TEXT,
        days INTEGER,
        interests TEXT,
        people INTEGER,
        currency TEXT,
        budget INTEGER,
        weather TEXT,
        itinerary TEXT,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Username already exists
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == password:
        return True
    return False

def save_itinerary(username, location, start_date, days, interests, people, currency, budget, weather, itinerary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    interests_str = ",".join(interests) if isinstance(interests, (list, tuple)) else str(interests)
    cursor.execute("""
        INSERT INTO itineraries (username, location, start_date, days, interests, people, currency, budget, weather, itinerary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, location, start_date, days, interests_str, people, currency, budget, weather, itinerary))
    conn.commit()
    conn.close()

def get_user_itineraries(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id,location, start_date, days, interests, people, currency, budget, weather, itinerary
        FROM itineraries
        WHERE username = ?
        ORDER BY start_date DESC
    """, (username,))
    trips = cursor.fetchall()
    conn.close()
    return trips
