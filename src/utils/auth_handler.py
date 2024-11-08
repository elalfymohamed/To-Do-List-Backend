import jwt
from datetime import datetime, timezone,timedelta
from core.security import security_config

def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token,
            security_config.SECRET_KEY,
            algorithms=[security_config.ALGORITHM],
            options={"verify_exp": False}  
        )

        if 'expires' in decoded_token:
            expiration_time = datetime.fromtimestamp(decoded_token['expires'], tz=timezone.utc)
            if expiration_time < datetime.now(tz=timezone.utc):
                return None  

        return decoded_token
    
    except jwt.ExpiredSignatureError:
        # Token has expired, return None
        return None
    
    except jwt.JWTError:
        # Catch any other JWT errors (invalid token format, etc.)
        return None
    




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)  # 30 days
    to_encode.update({"expires": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, security_config.SECRET_KEY, algorithm=security_config.ALGORITHM)
    return encoded_jwt
