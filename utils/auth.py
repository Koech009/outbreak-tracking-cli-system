from utils.file_handler import load_json, save_json
import hashlib, os
from datetime import datetime

def is_valid_email(email):
    index_1 = email.find("@")
    index_2 = email.find(".")
    if index_2 > index_1 + 1:  
        return True
    return False

def register_user(name, email, password, role):
    users = load_json("data/users.json")
    
    if not is_valid_email(email):
        raise ValueError("Invalid email format.")
    
    if any(u["email"] == email for u in users):
        raise ValueError("This email already exists.")
    
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    
    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password_hash": hashed,   
        "salt": salt,
        "role": role,
        #what does .iso format look like?
        "created_at": datetime.now().isoformat()   
    }
    
    users.append(user) 
    #why do we need to save the entire list and not just the new thing to the list since it was already saved before?                         
    save_json("data/users.json", users)         
    print("User registered successfully.")

def login_user(email, password):
    users = load_json("data/users.json")
    
    match = next((user for user in users if user["email"] == email), None)
    
    if match is None:
        raise ValueError("Email does not exist, please try again.")
    
    
    new_hash = hashlib.sha256((match["salt"] + password).encode()).hexdigest()
    
    if new_hash == match["password_hash"]:    
        return {
            "id": match["id"],                
            "name": match["name"],
            "email": match["email"],
            "role": match["role"]
        }
    else:
        raise ValueError("Incorrect password, please try again!")


        
    
         
     