import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.sqlite')

class UserManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def init_db(self):
        """Initialize database with users table"""
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                location TEXT,
                is24HourFormat BOOL DEFAULT 1,
                isMetricSystem BOOL DEFAULT 1,
                setupWizardDone BOOL DEFAULT 0,
                refreshRate_minutes INT DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()
        self.conn.close()
    
    def create_user(self, username, email, password_hash, location='', is24HourFormat=True, isMetricSystem=True, setupWizardDone=False, refreshRate_minutes=60):
        """Create a new user"""
        querry = """SELECT id FROM users WHERE id"""
        if not querry:
            self.cursor.execute("""
                INSERT INTO users (username, email, password_hash, location, is24HourFormat, isMetricSystem, setupWizardDone, refreshRate_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, location, is24HourFormat, isMetricSystem, setupWizardDone, refreshRate_minutes))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            self.conn.close()
            return user_id
        else:
            return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""SELECT * FROM users WHERE id = ?""", (user_id,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result
    
    def update_user(self, user_id, **kwargs):
        """Update user fields"""
        allowed_fields = ['username', 'email', 'location', 'is24HourFormat', 'isMetricSystem', 'setupWizardDone', 'refreshRate_minutes']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        
        self.cursor.execute(f"""UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?""", values)
        self.conn.commit()
        success = self.cursor.rowcount > 0
        self.conn.close()
        return success
    
    def delete_user(self, user_id):
        """Delete user by ID"""
        self.cursor.execute("""DELETE FROM users WHERE id = ?""", (user_id,))
        self.conn.commit()
        success = self.cursor.rowcount > 0
        self.conn.close()
        return success

# Initialize manager
user_manager = UserManager()