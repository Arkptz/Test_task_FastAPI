import time

import jwt
from config import secret, algorithm


JWT_SECRET = secret
JWT_ALGORITHM = algorithm

def token_response(token: str):
    return {
        "access_token": token
    }



def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}