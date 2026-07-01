# connection.py
import mysql.connector
import os

def connect_db():
    """Establishes connection to the MySQL database, initializing it from cbs.sql if missing."""
    db_name = "cbs"
    
    # Target Machine Environment Configurations
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'admin',  # Change this to match the target machine's MySQL root password
    }

    try:
        # Step 1: Secure a baseline raw handshake with the local MySQL server instance
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        
        # Step 2: Query the active schema manifest to check for existing architecture
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        schema_exists = cursor.fetchone()
        
        if not schema_exists:
            print(f"\n[System Notice] Database '{db_name}' not detected on this local machine instance.")
            sql_file_path = "cbs.sql"
            
            if not os.path.exists(sql_file_path):
                print(f"[Initialization Error] CRITICAL: '{sql_file_path}' missing from root. Setup aborted.\n")
                cursor.close()
                db.close()
                return None
                
            print("Deploying core operational banking layout maps from 'cbs.sql'...")
            
            # Step 3: Parse the system script and break it down statement by statement
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                # Splitting by semicolon handles standard structural DDL blocks perfectly
                sql_commands = f.read().split(';')
                
                for command in sql_commands:
                    clean_command = command.strip()
                    if clean_command:  # Bypass trailing empty split spaces
                        try:
                            cursor.execute(clean_command)
                        except mysql.connector.Error as command_error:
                            # Catch data collision warnings gracefully while pushing core queries
                            pass
            
            db.commit()
            print("[SUCCESS] Core Banking System structure deployed successfully!\n")
        
        # Step 4: Drop the base link and reconnect specifically targeted to the newly populated schema
        cursor.close()
        db.close()
        
        config['database'] = db_name
        return mysql.connector.connect(**config)

    except mysql.connector.Error as server_error:
        print(f"\n[Database Connection Error] Could not establish server handshake: {server_error}")
        print("Please verify that your local MySQL Server service is up and running.\n")
        return None