import bcrypt
from database.mongo import users_collection

# Procurar utilizador pelo nome
def find_user(username):
    return users_collection.find_one({"username": username})

# Verificar password (usada no login)
def verify_password(username, password):
    user = find_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return True
    return False

# Registar novo utilizador
def add_user(username, password):
    if find_user(username):
        return False  # Já existe

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users_collection.insert_one({
        "username": username,
        "password": hashed
    })
    return True
