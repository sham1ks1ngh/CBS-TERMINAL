# status.py
import pymysql
from connection import connect_db

def manage_entity_status(table_name, id_column_name, entity_label):
    """Generic engine to view, block, or unblock system account records."""
    target_id = input(f"\nEnter Target {entity_label} ID: ").strip()
    
    db = connect_db()
    if not db:
        return
    
    # FIX: Explicitly naming the 'cursor' keyword argument for PyMySQL
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    
    try:
        # 1. Fetch current status profile
        if table_name == "employees":
            query = f"SELECT fname, lname, username, status FROM {table_name} WHERE {id_column_name} = %s"
        else:
            query = f"SELECT acc_holder, status FROM {table_name} WHERE {id_column_name} = %s"
            
        cursor.execute(query, (target_id,))
        record = cursor.fetchone()
        
        if not record:
            print(f"\n[Record Error] No {entity_label} matched ID: {target_id}\n")
            return
            
        name = f"{record['fname']} {record['lname']}" if table_name == "employees" else record['acc_holder']
        print("\n" + "="*40)
        print(f"        {entity_label.upper()} STATUS ACCESS PROFILE       ")
        print("="*40)
        print(f"Target Name    : {name}")
        print(f"Account Status : {record['status'].upper()}")
        print("="*40)
        
        print("\nManagement Operations:")
        print("1. Leave Status Unchanged")
        print("2. BLOCK Account Access")
        print("3. UNBLOCK / Reactivate Account")
        choice = input("Select processing path (1/2/3): ").strip()
        
        new_status = None
        if choice == "2":
            new_status = "BLOCKED"
        elif choice == "3":
            new_status = "ACTIVE"
            
        if new_status:
            if record['status'].upper() == new_status:
                print(f"\n[Status Notice] Account state is already marked as {new_status}.\n")
                return
                
            # Update target record status inside active connection instance
            update_query = f"UPDATE {table_name} SET status = %s WHERE {id_column_name} = %s"
            cursor.execute(update_query, (new_status, target_id))
            db.commit()
            print(f"\n[SUCCESS] {entity_label} status updated to '{new_status}' safely.\n")
            
    except pymysql.MySQLError as err:
        print(f"[Database Write Error] Status update execution failed: {err}\n")
    finally:
        cursor.close()
        db.close()


def status_menu_portal(user_right):
    """Sub-interface workspace triggered via the -status command."""
    # Strict Guard Rail Check - Admin Only Access Gateway
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Clearance Violation: Only Administrators can modify status maps.\n")
        return
        
    print("\n" + "="*15 + " ADMINISTRATIVE SYSTEM STATUS ENGINE " + "="*15)
    print("1. Manage Employee Accounts (Staff)")
    print("2. Manage Customer Accounts (Bank Accounts)")
    print("="*68)
    
    choice = input("Select context module (1 or 2): ").strip()
    if choice == "1":
        manage_entity_status("employees", "emp_id", "Employee")
    elif choice == "2":
        manage_entity_status("customers", "acc_id", "Customer")
    else:
        print("[Invalid Choice] Returning to master runtime shell prompt loop.\n")
