from fastapi import HTTPException, status,Request
from core.security import security_config
import jwt

async def ValidateAccessToken(request: Request) -> Request:
        
        access_token =  request.headers.get('Authorization') 

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Not authenticated'
            )

        access_token = access_token.split(' ')

        is_valid_signature = jwt.decode(access_token[1], security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM])


        if not is_valid_signature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid access token'
            )
        
        return request

