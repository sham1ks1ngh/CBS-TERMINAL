# banking_operations.py
import mysql.connector
from connection import connect_db

def execute_credit():
    """Deposits cash into a customer account."""
    print("\n" + "-"*15 + " CASH DEPOSIT (CREDIT) " + "-"*15)
    acc_id = input("Enter Customer Account ID: ").strip()
    try:
        amount = float(input("Enter Amount to Deposit (₹): ").strip())
        if amount <= 0:
            print("[Validation Error] Amount must be greater than zero.\n")
            return
    except ValueError:
        print("[Validation Error] Invalid numeric amount entered.\n")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT acc_holder FROM customers WHERE acc_id = %s", (acc_id,))
        customer = cursor.fetchone()
        if not customer:
            print(f"[Record Error] Account ID {acc_id} does not exist.\n")
            return

        cursor.execute("""
            UPDATE customers 
            SET current_balance = current_balance + %s, total_transactions = total_transactions + 1 
            WHERE acc_id = %s
        """, (amount, acc_id))

        cursor.execute("""
            INSERT INTO transactions (sender_acc, receiver_acc, txn_type, amount) 
            VALUES (NULL, %s, 'credit', %s)
        """, (acc_id, amount))

        db.commit()
        print(f"[SUCCESS] ₹{amount:,.2f} credited successfully to Account {acc_id}!\n")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"[Transaction Failed] Database safety rollback executed. Error: {err}\n")
    finally:
        cursor.close()
        db.close()


def execute_debit():
    """Withdraws cash from a customer account with strict overdraft checks."""
    print("\n" + "-"*15 + " CASH WITHDRAWAL (DEBIT) " + "-"*15)
    acc_id = input("Enter Customer Account ID: ").strip()
    try:
        amount = float(input("Enter Amount to Withdraw (₹): ").strip())
        if amount <= 0:
            print("[Validation Error] Amount must be greater than zero.\n")
            return
    except ValueError:
        print("[Validation Error] Invalid numeric amount entered.\n")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT acc_holder, current_balance FROM customers WHERE acc_id = %s", (acc_id,))
        customer = cursor.fetchone()
        if not customer:
            print(f"[Record Error] Account ID {acc_id} does not exist.\n")
            return

        if float(customer['current_balance']) < amount:
            print(f"[INSUFFICIENT FUNDS] Account has ₹{float(customer['current_balance']):,.2f}. Cannot debit ₹{amount:,.2f}.\n")
            return

        cursor.execute("""
            UPDATE customers 
            SET current_balance = current_balance - %s, total_transactions = total_transactions + 1 
            WHERE acc_id = %s
        """, (amount, acc_id))

        cursor.execute("""
            INSERT INTO transactions (sender_acc, receiver_acc, txn_type, amount) 
            VALUES (%s, NULL, 'debit', %s)
        """, (acc_id, amount))

        db.commit()
        print(f"[SUCCESS] ₹{amount:,.2f} debited safely from Account {acc_id}!\n")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"[Transaction Failed] Database safety rollback executed. Error: {err}\n")
    finally:
        cursor.close()
        db.close()


def execute_transfer():
    """Transfers funds between two distinct customer accounts safely using atomic grouping."""
    print("\n" + "-"*15 + " ACCOUNT-TO-ACCOUNT TRANSFER " + "-"*15)
    sender_id = input("Enter Sender Account ID: ").strip()
    receiver_id = input("Enter Receiver Account ID: ").strip()
    
    if sender_id == receiver_id:
        print("[Validation Error] Sender and Receiver accounts cannot be the same.\n")
        return

    try:
        amount = float(input("Enter Amount to Transfer (₹): ").strip())
        if amount <= 0:
            print("[Validation Error] Amount must be greater than zero.\n")
            return
    except ValueError:
        print("[Validation Error] Invalid numeric amount entered.\n")
        return

    db = connect_db()
    if not db:
        return
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT acc_holder, current_balance FROM customers WHERE acc_id = %s", (sender_id,))
        sender = cursor.fetchone()
        if not sender:
            print(f"[Record Error] Sender Account ID {sender_id} does not exist.\n")
            return

        if float(sender['current_balance']) < amount:
            print(f"[INSUFFICIENT FUNDS] Sender has ₹{float(sender['current_balance']):,.2f}. Cannot transfer ₹{amount:,.2f}.\n")
            return

        cursor.execute("SELECT acc_holder FROM customers WHERE acc_id = %s", (receiver_id,))
        receiver = cursor.fetchone()
        if not receiver:
            print(f"[Record Error] Receiver Account ID {receiver_id} does not exist.\n")
            return

        cursor.execute("UPDATE customers SET current_balance = current_balance - %s, total_transactions = total_transactions + 1 WHERE acc_id = %s", (amount, sender_id))
        cursor.execute("UPDATE customers SET current_balance = current_balance + %s, total_transactions = total_transactions + 1 WHERE acc_id = %s", (amount, receiver_id))
        cursor.execute("INSERT INTO transactions (sender_acc, receiver_acc, txn_type, amount) VALUES (%s, %s, 'transfer', %s)", (sender_id, receiver_id, amount))

        db.commit()
        print(f"[SUCCESS] Inter-account transfer complete! ₹{amount:,.2f} moved from {sender_id} to {receiver_id}.\n")
    except mysql.connector.Error as err:
        db.rollback()
        print(f"[CRITICAL ERROR] Inter-account routing malfunction. Transaction rolled back. Details: {err}\n")
    finally:
        cursor.close()
        db.close()


def view_transaction_history():
    """Queries and formats ledger data matching parameters inside an organized datagrid table."""
    print("\n" + "-"*15 + " LEDGER STATEMENT PORTAL " + "-"*15)
    print("1. Search Statements by Single Account ID")
    print("2. View All Global Bank Logs (Master Audit)")
    mode = input("Choose selection tier (1/2): ").strip()
    
    db = connect_db()
    if not db:
        return
    cursor = db.cursor(dictionary=True)
    
    try:
        if mode == "1":
            acc_id = input("Enter Target Account ID: ").strip()
            # Find rows where the account was either the sender OR the receiver
            query = """
                SELECT txn_id, COALESCE(sender_acc, 'CASH') as sender, COALESCE(receiver_acc, 'CASH') as receiver, 
                       txn_type, amount, timestamp 
                FROM transactions 
                WHERE sender_acc = %s OR receiver_acc = %s
                ORDER BY timestamp DESC
            """
            cursor.execute(query, (acc_id, acc_id))
        elif mode == "2":
            query = """
                SELECT txn_id, COALESCE(sender_acc, 'CASH') as sender, COALESCE(receiver_acc, 'CASH') as receiver, 
                       txn_type, amount, timestamp 
                FROM transactions 
                ORDER BY timestamp DESC
            """
            cursor.execute(query)
        else:
            print("[Invalid Option] Aborting statement extraction loop.\n")
            return

        rows = cursor.fetchall()
        if not rows:
            print("\n[Audit Alert] No ledger history entries match these parameters.\n")
            return
            
        # Display Grid Table Parameters
        header_format = "| {:<7} | {:<12} | {:<12} | {:<10} | {:>14} | {:<21} |"
        row_format    = "| {:<7} | {:<12} | {:<12} | {:<10} | {:>14,.2f} | {:<21} |"
        border = "-" * 88
        
        print(f"\n{border}")
        print(header_format.format("TXN ID", "SENDER", "RECEIVER", "TYPE", "AMOUNT (₹)", "TIMESTAMP"))
        print(border)
        
        for row in rows:
            # Re-format timestamp string for presentation clarity
            ts_str = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if row['timestamp'] else 'N/A'
            print(row_format.format(
                row['txn_id'],
                str(row['sender']),
                str(row['receiver']),
                row['txn_type'].upper(),
                float(row['amount']),
                ts_str
            ))
        print(border + "\n")
        
    except mysql.connector.Error as err:
        print(f"[Ledger Query Failure] System error reading transactions table: {err}\n")
    finally:
        cursor.close()
        db.close()


def transaction_menu_portal():
    """Sub-interface workspace triggered via the -transaction command."""
    print("\n" + "="*15 + " FINANCIAL TRANSACTION ENGINE " + "="*15)
    print("1. Cash Deposit (Credit)")
    print("2. Cash Withdrawal (Debit)")
    print("3. Fund Transfer (Account to Account)")
    print("4. View Statement / Transaction History Logs")
    print("="*58)
    
    choice = input("Select processing option (1/2/3/4): ").strip()
    if choice == "1":
        execute_credit()
    elif choice == "2":
        execute_debit()
    elif choice == "3":
        execute_transfer()
    elif choice == "4":
        view_transaction_history()
    else:
        print("[Invalid Entry] Cancelling operation. Returning to master loop.\n")