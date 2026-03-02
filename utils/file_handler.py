# import json

# def load_json(filepath):
#     try:
#         with open(filepath, "r") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []

# def save_json(filepath, data):
#     with open(filepath, "w") as f:
#         json.dump(data, f, indent=4)

import json

def load_json(filepath):
    try: 
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

