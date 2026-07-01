# customer_info.py (Append/Update these sections)
import mysql.connector
from connection import connect_db

def add_new_customer(user_right):
    """Allows administrators to register a brand new customer account entry."""
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Exception: Only Admins can register new customer records.\n")
        return

    print("\n" + "-"*15 + " REGISTER NEW CUSTOMER " + "-"*15)
    name = input("Enter Full Name: ").strip()
    sex = input("Enter Gender (M/F/O): ").strip().upper()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
    address = input("Enter Residential Address: ").strip()
    try:
        opening_balance = float(input("Enter Opening Deposit Balance (₹): ").strip())
        if opening_balance < 0:
            print("[Validation Error] Opening balance cannot be negative.\n")
            return
    except ValueError:
        print("[Validation Error] Invalid currency format.\n")
        return

    if not (name and sex and dob and address):
        print("[Validation Error] All fields are mandatory.\n")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    # Query excludes acc_id so MySQL AUTO_INCREMENT triggers automatically
    query = """
        INSERT INTO customers (acc_holder, sex, dob, address, current_balance, total_transactions, status)
        VALUES (%s, %s, %s, %s, %s, 0, 'ACTIVE')
    """
    try:
        cursor.execute(query, (name, sex, dob, address, opening_balance))
        db.commit()
        # Fetch the automatically generated ID
        new_id = cursor.lastrowid
        print(f"\n[SUCCESS] New customer registered successfully! Assigned Account ID: {new_id}\n")
    except mysql.connector.Error as err:
        print(f"[Database Error] Could not register account: {err}\n")
    finally:
        cursor.close()
        db.close()


def remove_customer(user_right):
    """Permanently deletes a customer file from the system database ledger."""
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Exception: Only Admins can drop customer entries.\n")
        return

    print("\n" + "-"*15 + " PERMANENTLY REMOVE CUSTOMER ACCOUNT " + "-"*15)
    acc_id = input("Enter Target Account ID to Delete: ").strip()

    db = connect_db()
    if not db:
        return
    cursor = db.cursor()

    try:
        # Check existence first
        cursor.execute("SELECT acc_holder FROM customers WHERE acc_id = %s", (acc_id,))
        customer = cursor.fetchone()
        if not customer:
            print(f"[Record Error] No customer found with Account ID: {acc_id}\n")
            return

        confirm = input(f"Are you absolutely sure you want to delete account {acc_id} ({customer[0]})? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            cursor.execute("DELETE FROM customers WHERE acc_id = %s", (acc_id,))
            db.commit()
            print(f"[SUCCESS] Account ID {acc_id} has been completely removed from the core ledger.\n")
        else:
            print("Deletion aborted cleanly.\n")
    except mysql.connector.Error as err:
        print(f"[Database Error] Dependency violation or error: {err}\n")
    finally:
        cursor.close()
        db.close()


def customer_menu_portal(user_right):
    print("\n" + "-"*15 + " CUSTOMER MODULE " + "-"*15)
    print("1. View Specific Customer Profile")
    print("2. Print Master Table of Every Record")
    print("3. Edit Customer Details (Admin Only)")
    print("4. Add New Customer Account (Admin Only)")
    print("5. Remove Customer Account (Admin Only)")
    print("-"*47)
    
    choice = input("Enter option (1-5): ").strip()
    if choice == "1":
        # logic from previous step
        view_customer_details()
    elif choice == "2":
        # logic from previous step
        view_all_customers_table()
    elif choice == "3":
        edit_customer_details(user_right)
    elif choice == "4":
        add_new_customer(user_right)
    elif choice == "5":
        remove_customer(user_right)
    else:
        print("[Invalid Entry] Returning to operational base.\n")