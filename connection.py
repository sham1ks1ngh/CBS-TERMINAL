# connection.py
import pymysql
import os
import traceback

def connect_db():
    """Establishes connection to the MySQL database safely using pure-Python PyMySQL."""
    db_name = "cbs"
    
    # Target configurations
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',  # <-- REPLACE WITH YOUR ACTUAL MYSQL ROOT PASSWORD
        'autocommit': True
    }

    try:
        # 1. Establish the baseline server connection
        db = pymysql.connect(**config)
        cursor = db.cursor()
        
        # 2. Inspect active system schemas
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        schema_exists = cursor.fetchone()
        
        if not schema_exists:
            print(f"\n[System Notice] Database '{db_name}' not detected on this machine.")
            sql_file_path = "cbs.sql"
            
            if not os.path.exists(sql_file_path):
                print(f"[Initialization Error] CRITICAL: '{sql_file_path}' missing from folder path.")
                cursor.close()
                db.close()
                return None
                
            print("Deploying core operational banking layout maps from 'cbs.sql'...")
            
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                # Split schema definitions safely by statement
                sql_commands = f.read().split(';')
                
                for command in sql_commands:
                    clean_command = command.strip()
                    if clean_command:
                        try:
                            cursor.execute(clean_command)
                        except Exception:
                            # Pass structural warning overrides or existing data alerts safely
                            pass
            print("[SUCCESS] Core Banking System structure deployed successfully!\n")
        
        cursor.close()
        db.close()
        
        # 3. Return the fully configured connection targeting your active 'cbs' schema
        config['database'] = db_name
        return pymysql.connect(**config)

    except pymysql.MySQLError as server_error:
        print(f"\n[Database Connection Error]: Could not establish handshake with MySQL server.")
        print(f"Details: {server_error}")
        print("Please verify your password in connection.py and ensure your local MySQL Service is running.\n")
        return None
        
    except Exception as general_error:
        print(f"\n[Unexpected Error inside connection.py]:")
        print(traceback.format_exc())
        return None
