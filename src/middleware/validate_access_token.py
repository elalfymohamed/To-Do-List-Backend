from fastapi import HTTPException, status,Request
from utils.auth_handler import decode_jwt

async def ValidateAccessToken(request: Request) -> Request:
        access_token =  request.headers.get('authorization') 

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Not authenticated'
            )

        bearer, access_token = access_token.split(' ')

        if bearer != 'Bearer':
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

        is_valid_signature = decode_jwt(access_token)

        if not is_valid_signature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid access token'
            )
        
        return request

