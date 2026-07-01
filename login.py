# login.py
import pymysql
import traceback
from connection import connect_db

def validate_login(username, password):
    """Queries the MySQL database using safe pure-Python connector protocols."""
    try:
        db = connect_db()
        if not db:
            return False, None
        
        # DictCursor maps rows to column names matching user['right']
        cursor = db.cursor(pymysql.cursors.DictCursor)
        query = "SELECT username, `right` FROM employees WHERE username = %s AND pwd = %s"
        
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if user:
            return True, user['right']
        else:
            return False, None

    except pymysql.MySQLError as db_err:
        print(f"\n[Database Query Error inside login.py]: {db_err}")
        return False, None
    except Exception as general_err:
        print(f"\n[CRITICAL PYTHON CRASH INSIDE LOGIN.PY]:")
        print(traceback.format_exc())
        return False, None
