# login.py
import mysql.connector
from connection import connect_db

def validate_login(username, password):
    """Queries the MySQL database to verify employee credentials."""
    db = connect_db()
    if not db:
        return False, None
    
    # dictionary=True allows us to read rows using column names like user['right']
    cursor = db.cursor(dictionary=True)
    query = "SELECT username, `right` FROM employees WHERE username = %s AND pwd = %s"
    
    try:
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            return True, user['right']
        else:
            return False, None
    except mysql.connector.Error as err:
        print(f"\n[Database Query Error]: {err}")
        return False, None
    finally:
        cursor.close()
        db.close()