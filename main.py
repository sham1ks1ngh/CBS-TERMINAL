# main.py
import sys
import os
from help import print_help
from login import validate_login
from customer_info import customer_menu_portal
from employees_info import employee_menu_portal
from banking_operations import transaction_menu_portal
from status import status_menu_portal  # Import the new status management engine

def clear_terminal():
    """Clears the terminal screen regardless of the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def intro_page():
    clear_terminal()
    print("*" * 50)
    print("      WELCOME TO THE CORE BANKING SYSTEM (CBS)     ")
    print("*" * 50)
    print("\nType '-help' at any time to see available options.\n")

    is_authenticated = False
    current_user = None
    user_role = None

    while True:
        prompt = f"CBS-System ({current_user if current_user else 'Guest'}) > "
        command = input(prompt).strip().lower()

        if command == "-help":
            print_help(context="intro", is_authenticated=is_authenticated, user_role=user_role)
        
        elif command == "-clear":
            clear_terminal()
            
        elif command == "-exit":
            print("Exiting system safely. Goodbye!")
            sys.exit()
            
        elif command == "-login":
            if is_authenticated:
                print(f"\nYou are already securely logged in as {current_user}. Use '-logout' first.\n")
                continue
                
            print("\n" + "-"*15 + " LOGIN WINDOW " + "-"*15)
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            try:
                result = validate_login(username, password)
                
                if result and isinstance(result, tuple):
                    success, user_right = result
                else:
                    success, user_right = False, None
                
                if success:
                    is_authenticated = True
                    current_user = username
                    user_role = user_right
                    
                    print("\n" + "="*40)
                    print("         ACCESS GRANTED SUCCESSFULLY       ")
                    print("="*40)
                    print(f"User    : {current_user}")
                    print(f"Rights  : {user_role.upper()}")
                    print("="*40 + "\n")
                else:
                    print("\n[Access Denied] Invalid username or password. Please try again.\n")
                    
            except Exception as e:
                print(f"\n[System Error] Internal interface loop handling malfunction: {e}\n")
        
        elif command == "-logout":
            if not is_authenticated:
                print("\n[Session Error] You are not currently logged into any session.\n")
                continue
                
            confirm = input(f"Are you sure you want to log out of account '{current_user}'? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                print(f"\n[LOGOUT] Session for '{current_user}' cleared successfully.")
                is_authenticated = False
                current_user = None
                user_role = None
                print("Returning to Guest access tier.\n")
            else:
                print("\nLogout cancelled. Session remains active.\n")
        
        elif command == "-customer":
            if not is_authenticated:
                print("\n[Authentication Error] You must run '-login' successfully before viewing files.\n")
            else:
                customer_menu_portal(user_role)
                
        elif command == "-employee":
            if not is_authenticated:
                print("\n[Authentication Error] Security exception: Session unauthenticated.\n")
            else:
                employee_menu_portal(user_role)
                
        elif command == "-transaction":
            if not is_authenticated:
                print("\n[Authentication Error] Unauthenticated access denied. Please login first.\n")
            else:
                transaction_menu_portal()
                
        elif command == "-status":  # Capture status command route parameters
            if not is_authenticated:
                print("\n[Authentication Error] Admin security verification missing.\n")
            else:
                status_menu_portal(user_role)
                
        else:
            print("[Invalid Command] Type '-help' to review authorized operators.")

if __name__ == "__main__":
    intro_page()