import sqlite3


class Database:
    def __init__(self, db_name="chat.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                channel TEXT NOT NULL,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()

    def add_user(self, username, password):
        self.conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        self.conn.commit()

    def verify_user(self, username, password):
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        return cursor.fetchone() is not None

    def add_message(self, channel, username, content):
        self.conn.execute(
            "INSERT INTO messages (channel, username, content) VALUES (?, ?, ?)",
            (channel, username, content),
        )
        self.conn.commit()

    def get_messages(self, channel, limit=50):
        cursor = self.conn.execute(
            "SELECT * FROM messages WHERE channel = ? ORDER BY timestamp DESC LIMIT ?",
            (channel, limit),
        )
        return cursor.fetchall()
