import sqlite3

# Database path
DB_PATH = "sources\\backend\\DATABASES\\users.sqlite"

class UserManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def init_db(self):
        """Initialize database with users table"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                location TEXT,
                city TEXT,
                is24HourFormat BOOL DEFAULT 1,
                isMetricSystem BOOL DEFAULT 1,
                setupWizardDone BOOL DEFAULT 0,
                refreshRate_minutes INT DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()
        # self.conn.close()
    
    def create_user(self, username, email, password_hash, location='', is24HourFormat=True, isMetricSystem=True, setupWizardDone=False, refreshRate_minutes=60):
        """Create a new user"""
        query = """SELECT id FROM users WHERE username = ? OR email = ?"""
        self.cursor.execute(query, (username, email))
        user_info = self.cursor.fetchall()
        if not user_info:
            self.cursor.execute("""
                INSERT INTO users (username, email, password_hash, location, is24HourFormat, isMetricSystem, setupWizardDone, refreshRate_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, location, is24HourFormat, isMetricSystem, setupWizardDone, refreshRate_minutes))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            return user_id
        else:
            return None
        
    
    def get_user(self, user_id):
        """Get user by ID"""
        self.cursor.execute(
            """
                SELECT
                    id,
                    username,
                    email,
                    password_hash,
                    location,
                    is24HourFormat,
                    isMetricSystem,
                    setupWizardDone,
                    refreshRate_minutes,
                    city
                FROM users
                WHERE id = ?
            """,
            (user_id,),
        )
        result = self.cursor.fetchone()
        return result
    
    def update_user(
        self,
        user_id,
        username=None,
        email=None,
        location=None,
        is24HourFormat=None,
        isMetricSystem=None,
        setupWizardDone=None,
        refreshRate_minutes=None,
        city=None,
    ):
        """Update user fields (pass only values to change)"""
        updates = {
            'username': username,
            'email': email,
            'location': location,
            'is24HourFormat': is24HourFormat,
            'isMetricSystem': isMetricSystem,
            'setupWizardDone': setupWizardDone,
            'refreshRate_minutes': refreshRate_minutes,
            'city': city,
        }
        filtered_updates = {}
        for key, value in updates.items():
            if value is not None:
                filtered_updates[key] = value
        updates = filtered_updates
        
        if not updates:
            return False
        
        set_parts = []
        for key in updates.keys():
            set_parts.append(f'{key} = ?')
        set_clause = ', '.join(set_parts)
        values = list(updates.values()) + [user_id]
        
        self.cursor.execute(f"""UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?""", values)
        self.conn.commit()
        success = self.cursor.rowcount > 0
        return success

    def update_user_city(self, user_id, city):
        """Update the user's city (can be None)"""
        self.cursor.execute(
            """
                UPDATE users
                SET city = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
            (city, user_id),
        )
        self.conn.commit()
        success = self.cursor.rowcount > 0
        return success
    
    def delete_user(self, user_id):
        """Delete user by ID"""
        self.cursor.execute("""DELETE FROM users WHERE id = ?""", (user_id))
        self.conn.commit()
        success = self.cursor.rowcount > 0
        return success


# user = UserManager()
# user.create_user("kaelig", "kaelig@nsi.fr", "password_hash", location='48, -1.8')