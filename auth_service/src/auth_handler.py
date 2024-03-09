# This file is responsible for signing , encoding , decoding and returning JWTS
import time
import os
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = os.getenv("AUTH_SECRET") if os.getenv("AUTH_SECRET") != None else ""
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    print(JWT_SECRET, JWT_ALGORITHM, payload)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}