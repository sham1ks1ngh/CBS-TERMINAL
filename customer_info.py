# customer_info.py
import pymysql
from connection import connect_db

def view_customer_details():
    """Fetches and displays the specific profile metrics of a target customer entry."""
    print("\n" + "-"*15 + " VIEW CUSTOMER PROFILE " + "-"*15)
    acc_id = input("Enter Customer Account ID: ").strip()

    db = connect_db()
    if not db:
        return
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM customers WHERE acc_id = %s", (acc_id,))
        row = cursor.fetchone()

        if row:
            print("\n" + "="*40)
            print(f"ACCOUNT HOLDER : {row['acc_holder']}")
            print(f"ACCOUNT ID     : {row['acc_id']}")
            print(f"GENDER (SEX)   : {row['sex']}")
            print(f"DATE OF BIRTH  : {row['dob']}")
            print(f"RESIDENCE ADDR : {row['address']}")
            print(f"CURRENT BALANCE: ₹{row['current_balance']:.2f}")
            print(f"TOTAL LOGS     : {row['total_transactions']} logs")
            print(f"LEDGER STATUS  : {row['status']}")
            print("="*40 + "\n")
        else:
            print(f"[Record Error] No customer found matching Account ID: {acc_id}\n")
    except pymysql.MySQLError as err:
        print(f"[Database Error] Query execution failure: {err}\n")
    finally:
        cursor.close()
        db.close()

def view_all_customers_table():
    """Prints a structured tabular master ledger overview of all customers."""
    db = connect_db()
    if not db:
        return
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT acc_id, acc_holder, current_balance, status FROM customers")
        rows = cursor.fetchall()

        if rows:
            print("\n" + "="*70)
            print(f"{'ACC ID':<8} | {'ACCOUNT HOLDER':<25} | {'BALANCE':<15} | {'STATUS':<10}")
            print("="*70)
            for row in rows:
                print(f"{row['acc_id']:<8} | {row['acc_holder']:<25} | ₹{row['current_balance']:<14.2f} | {row['status']:<10}")
            print("="*70 + "\n")
        else:
            print("[System Alert] The core customer database ledger is currently empty.\n")
    except pymysql.MySQLError as err:
        print(f"[Database Error] Table compilation failure: {err}\n")
    finally:
        cursor.close()
        db.close()

def edit_customer_details(user_right):
    """Allows administrators to update a customer's address profile information."""
    if user_right.lower() != "admin":
        print("\n[ACCESS DENIED] Security Exception: Only Admins can modify customer indices.\n")
        return

    print("\n" + "-"*15 + " EDIT CUSTOMER PROFILE " + "-"*15)
    acc_id = input("Enter Customer Account ID to Update: ").strip()

    db = connect_db()
    if not db:
        return
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT acc_holder, address FROM customers WHERE acc_id = %s", (acc_id,))
        row = cursor.fetchone()

        if not row:
            print(f"[Record Error] No customer found matching Account ID: {acc_id}\n")
            return

        print(f"Current Address for {row['acc_holder']}: {row['address']}")
        new_address = input("Enter New Residential Address: ").strip()

        if not new_address:
            print("[Update Aborted] Address input field cannot be left blank.\n")
            return

        cursor.execute("UPDATE customers SET address = %s WHERE acc_id = %s", (new_address, acc_id))
        db.commit()
        print(f"[SUCCESS] Core profile address for Account ID {acc_id} has been modified.\n")
    except pymysql.MySQLError as err:
        print(f"[Database Error] Modification write failed: {err}\n")
    finally:
        cursor.close()
        db.close()

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

    query = """
        INSERT INTO customers (acc_holder, sex, dob, address, current_balance, total_transactions, status)
        VALUES (%s, %s, %s, %s, %s, 0, 'ACTIVE')
    """
    try:
        cursor.execute(query, (name, sex, dob, address, opening_balance))
        db.commit()
        new_id = cursor.lastrowid
        print(f"\n[SUCCESS] New customer registered successfully! Assigned Account ID: {new_id}\n")
    except pymysql.MySQLError as err:
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
    except pymysql.MySQLError as err:
        print(f"[Database Error] Dependency violation or error: {err}\n")
    finally:
        cursor.close()
        db.close()

def customer_menu_portal(user_right):
    """Main routing dashboard terminal loop for Customer Account metrics."""
    print("\n" + "-"*15 + " CUSTOMER MODULE " + "-"*15)
    print("1. View Specific Customer Profile")
    print("2. Print Master Table of Every Record")
    print("3. Edit Customer Details (Admin Only)")
    print("4. Add New Customer Account (Admin Only)")
    print("5. Remove Customer Account (Admin Only)")
    print("-"*47)
    
    choice = input("Enter option (1-5): ").strip()
    if choice == "1":
        view_customer_details()
    elif choice == "2":
        view_all_customers_table()
    elif choice == "3":
        edit_customer_details(user_right)
    elif choice == "4":
        add_new_customer(user_right)
    elif choice == "5":
        remove_customer(user_right)
    else:
        print("[Invalid Entry] Returning to operational base.\n")
