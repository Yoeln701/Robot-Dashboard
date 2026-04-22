import sqlite3

DB_NAME = "logs.db"

# ------------------ INIT ------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Logs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            command TEXT
        )
    """)

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()

# ------------------ LOG COMMAND ------------------
def log_command(user, command):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO logs (user, command) VALUES (?, ?)",
        (user, command)
    )

    conn.commit()
    conn.close()


# ------------------ GET LOGS ------------------
def get_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT user, command FROM logs ORDER BY id DESC LIMIT 10")
    logs = c.fetchall()

    conn.close()
    return logs

# ------------------ USERS ------------------
def create_user(username, password, role):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )

    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    )

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "username": row[0],
            "password": row[1],
            "role": row[2]
        }
    return None