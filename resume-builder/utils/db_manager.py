import sqlite3
import bcrypt
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path='users.db'):
        self.db_path = self._resolve_db_path(db_path)
        self._init_db()

    def _resolve_db_path(self, db_path):
        """Resolve the database path relative to the project and ensure its directory exists."""
        path = Path(db_path)
        if not path.is_absolute():
            project_root = Path(__file__).resolve().parent.parent
            path = project_root / path

        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _get_connection(self):
        """Create a SQLite connection for the configured database path."""
        return sqlite3.connect(self.db_path)
    
    def _init_db(self):
        """Initialize the database and create tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def create_user(self, username, password, email):
        """Create a new user"""
        try:
            # Hash the password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                    (username, password_hash, email)
                )
                
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username or email already exists
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
                result = cursor.fetchone()
            
            if result:
                stored_hash = result[0].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
            return False
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False
    
    def user_exists(self, username=None, email=None):
        """Check if a user exists by username or email"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                if username:
                    cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
                elif email:
                    cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
                else:
                    return False
                
                result = cursor.fetchone() is not None
                return result
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
