# 4:20–4:55 | Build the Registration Flow
# Your register_user function needs to: collect a name, email, password, and role,
# validate that the email isn't already taken (by loading users.json),
# hash the password,
# construct a user dictionary,
# and save it back to the file.
# A few Python things to really understand here: 
# you'll be calling your teammate's file_handler.py functions (load_json, save_json). 
# What does it mean to depend on another module? 
    # it means that i would need to import it...?
# How do you import it? 
    # by writing from. module_name import function names
# Think about what happens if the file doesn't exist yet — does load_json handle that, or should auth.py guard against it?
    #load_json handles it within its logic by returning an empty list if there's a filenotfounderror butttt is an empty list 
    # good ux or does the user never actually see that and is that just developer side...? 
    # also expound to me on how auth.py would guard against this?
# Also think about input validation as a first-class concern. 
# A function like is_valid_email(email) that returns a boolean is a clean, testable way to handle this. 
# Write it as a small helper inside auth.py. What makes an email valid? At minimum, it contains @ and a . after it.

from .file_handler import load_json, save_json
import hashlib, os

def is_valid_email(email):
     index_1 = email.find("@")
     index_2 = email.find(".")
     if index_2 > index_1:
          return True
     else:
          return False
     
def register_user(name, email, password, role):
     
     #starting with input validation
     users = load_json("data/user.json")

     if not is_valid_email(email):
          return
     
     if email in users:
          return "This email address already exists. Please try a different address."
     
     #password hashing section
     salt = os.urandom(16).hex()
     hashed = hashlib.sha256((salt+password).encode()).hexdigest()

     #creating a user dictionary
     user = {
          "name": name,
          "email": email,
          "hashed": hashed,
          "salt": salt,
          "role": role
     }

     save_json("data/user.json", user)

def login_user(name, password, role):
    pass
     