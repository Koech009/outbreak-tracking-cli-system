# 6:50–7:20 | Build the Menu Loop
# Start with the unauthenticated menu (Register / Login / Exit). 
# This is a while True loop that prints options, takes input, and calls the right function from auth.py. 
# When login succeeds, you get back a current_user dict. That dict has a role field.
# Now build role-based routing. A clean pattern here is a dictionary dispatch:
# menus = {
#     "admin": show_admin_menu,
#     "health_worker": show_health_worker_menu,
#     "community_user": show_community_menu
# }
# Then you call menus[current_user["role"]](). 
# This is cleaner than a long if/elif chain and teaches you about functions as first-class objects in Python 
# — one of the language's most powerful features.

# Each sub-menu is its own function that also runs a loop until the user chooses Logout.

#pseudocode for while loop menu#

# while this loop is true:
    # show the menu options
    # ask for input
    # if the input is 1: call register_user from auth.py
    # if the input is 2: call login_user from auth.py
    # if the input is 3: break and say 'goodbye for now'
    # else print 'invalid input, please try again'

from utils.auth import register_user, login_user

def show_admin_menu(current_user):


def main ():
    while(True):
        print("1. Register\n 2.Login\n 3.Exit")
        choice = input("Please enter a number selection to proceed:\n> ")
        if choice == 1 or "register".tolower():
            name = input("Please enter your name\n> ")
            email = input("Please enter your email\n> ")
            password = input("Please create a password\n> ")
            role = input("Please enter your role\n> ")
            current_user = register_user(name, email, password, role)
        if choice == 2 or "login".tolower():
            name = input("Please enter your name\n> ")
            password = input("Please enter your password\n> ")
            role = input("Please enter your role\n> ")
            current_user = login_user(name, password, role)
        if choice == 3 or "exit".tolower():
            print("Goodbye")
            break
        else:
            print("Invalid input! Please try again.")

        menus = {
                "admin": show_admin_menu,
                "health_worker": show_health_worker_menu,
                "community_user": show_community_menu
                 }
        menus[current_user["role"]](current_user)

        
                                                    

            


if __name__ == "__main__":
    main()

