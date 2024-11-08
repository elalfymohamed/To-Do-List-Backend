from fastapi import HTTPException, status
from utils.auth_handler import decode_jwt

def decode_token(headers: dict) -> dict:
    """
    Checks that the authorization header contains a valid access token.
    If the token is invalid, it raises an HTTPException.
    Otherwise, it returns the decoded token data.
    """
    auth_header = headers.model_dump()

    auth_header = auth_header['authorization']

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    _, token = auth_header.split(' ')

    decoded_token = decode_jwt(token)

    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    return decoded_token

