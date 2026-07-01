# employees_info.py (Append/Update these sections)
import mysql.connector
from connection import connect_db

def add_new_employee(user_right):
    """Allows administrators to onboard a brand new employee worker."""
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Exception: Only Admins can onboard employees.\n")
        return

    print("\n" + "-"*15 + " ONBOARD NEW STAFF EMPLOYEE " + "-"*15)
    username = input("Create Login Username: ").strip()
    pwd = input("Set Temporary Password: ").strip()
    fname = input("Enter First Name: ").strip()
    lname = input("Enter Last Name: ").strip()
    dept_id = input("Assign Department Code (e.g., D01): ").strip().upper()
    role = input("System Access Clearance Tier (admin/staff): ").strip().lower()

    if role not in ['admin', 'staff']:
        print("[Validation Error] Clearance tier must be strictly 'admin' or 'staff'.\n")
        return

    if not (username and pwd and fname and lname and dept_id):
        print("[Validation Error] All input fields are required.\n")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    query = """
        INSERT INTO employees (username, pwd, fname, lname, dept_id, `right`, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVE')
    """
    try:
        cursor.execute(query, (username, pwd, fname, lname, dept_id, role))
        db.commit()
        new_emp_id = cursor.lastrowid
        print(f"\n[SUCCESS] Employee onboarded safely! Generated Employee ID: {new_emp_id}\n")
    except mysql.connector.Error as err:
        print(f"[Database Error] Integrity check failed. Username may already exist: {err}\n")
    finally:
        cursor.close()
        db.close()


def remove_employee(user_right):
    """Permanently offboards an employee from the system registry database."""
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Exception: Only Admins can delete personnel profiles.\n")
        return

    print("\n" + "-"*15 + " REMOVE WORKFORCE ACCOUNT " + "-"*15)
    emp_id = input("Enter Employee ID to Terminate: ").strip()

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    try:
        cursor.execute("SELECT fname, lname FROM employees WHERE emp_id = %s", (emp_id,))
        employee = cursor.fetchone()
        if not employee:
            print(f"[Record Error] No employee matched ID: {emp_id}\n")
            return

        confirm = input(f"Are you sure you want to delete profile for {employee[0]} {employee[1]}? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
            db.commit()
            print(f"[SUCCESS] Employee ID {emp_id} completely removed from access records.\n")
        else:
            print("Operation aborted safely.\n")
    except mysql.connector.Error as err:
        print(f"[Database Error] Could not isolate employee profile: {err}\n")
    finally:
        cursor.close()
        db.close()


def employee_menu_portal(user_right):
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Restricted Space: This portal requires Administrator clearance.\n")
        return
        
    print("\n" + "-"*15 + " EMPLOYEE MANAGEMENT PORTAL " + "-"*15)
    print("1. View Staff Member Profile")
    print("2. Print Master Table of All Staff")
    print("3. Edit Staff Record Parameters")
    print("4. Onboard New Employee (Admin Only)")
    print("5. Terminate/Remove Employee Account (Admin Only)")
    print("-"*58)
    
    choice = input("Enter option (1-5): ").strip()
    if choice == "1":
        view_employee_details()
    elif choice == "2":
        view_all_employees_table()
    elif choice == "3":
        edit_employee_details(user_right)
    elif choice == "4":
        add_new_employee(user_right)
    elif choice == "5":
        remove_employee(user_right)
    else:
        print("[Invalid Entry] Returning to basic prompt loop.\n")