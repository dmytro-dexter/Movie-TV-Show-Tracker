from datetime import datetime, timedelta
from jose import jwt


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "supersecret", algorithm="HS256")
    return encoded_jwt
