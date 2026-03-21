import json , os
STORAGE_FILE = 'user_session.json'

def save_user(user_id, phone, name):
    with open(STORAGE_FILE, 'w') as f:
        json.dump({'user_id' : user_id, 'name': name, 'user_phone': phone}, f)

def load_user():
    if not os.path.exists(STORAGE_FILE):
        return None
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def clear_user():
    if os.path.exists(STORAGE_FILE):
        os.remove(STORAGE_FILE)