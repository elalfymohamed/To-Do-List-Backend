import jwt

from datetime import datetime, timedelta, timezone, time

from core.security import security_config


def decode_jwt(token) -> dict | None:
    try:
        decoded_token = jwt.decode(token, security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM])

        if decoded_token["expires"] < time():
            return None
        
        return decoded_token
    
    except jwt.ExpiredSignatureError:
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




#   access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.model_dump()}, expires_delta=access_token_expires
#     )