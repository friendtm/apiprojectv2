import jwt
from datetime import datetime, timedelta

SECRET = "secret-key"

def gerar_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verificar_token(token):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded["sub"]
    except jwt.ExpiredSignatureError:
        return None
