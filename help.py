# help.py

def print_help(context="intro", is_authenticated=False, user_role=None):
    """Displays contextual help commands to the user."""
    print("\n" + "="*30 + " HELP MENU " + "="*30)
    
    if context == "intro":
        print("Available Guest Commands:")
        print("  -login       : Opens the secure authentication prompt.")
        print("  -clear       : Clears everything in the terminal window.")
        print("  -exit        : Safely terminates the banking application.")
        print("  -help        : Opens this diagnostic information display.")
        
        if is_authenticated:
            print("\nAuthenticated Operations:")
            print("  -customer    : Opens the customer accounts portal workspace.")
            print("  -transaction : Opens the cash posting and transfer engine.")
            print("  -logout      : Logs out of the current user session.")
            
            if user_role and user_role.lower() == "admin":
                print("  -employee    : Opens the privileged employee management portal.")
                print("  -status      : Opens the account restriction management window.")
            
    print("="*71 + "\n")