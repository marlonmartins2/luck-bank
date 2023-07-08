import base64

from typing import List

from fastapi_jwt_auth import AuthJWT

from pydantic import BaseModel

from fastapi import Depends, HTTPException, status

from settings import settings

from database.controllers.user import get_user_by_id

from utils import UserNotFound, NotVerified, UserDeleted

from utils.logger import Logger


logger = Logger.init('JWTLogger')


class JWTSettings(BaseModel):
    """
    settings from JWT authentication.

    Args:
        BaseModel (Pydantic): Base model class
    """
    authjwt_algorithm: str = settings.JWT_ALGORITHM

    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]

    authjwt_token_location: set = {'cookies', 'headers'}

    authjwt_access_cookie_key: str = 'access_token'

    authjwt_refresh_cookie_key: str = 'refresh_token'

    authjwt_cookie_csrf_protect: bool = False

    authjwt_denylist_enabled: bool = True

    authjwt_denylist_token_checks: set = {'access', 'refresh'}

    authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')

    authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return JWTSettings()


denylist = set()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist


def require_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        user = get_user_by_id(user_id)

        if user["deleted_at"]:
            raise UserDeleted('User deleted')

        if not user:
            raise UserNotFound('User no longer exist')

        if not user["is_active"]:
            raise NotVerified('You are not verified')

    except Exception as erro:
        error = erro.__class__.__name__
        logger.info(f'Error: {error}')

        if error == 'MissingTokenError':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')

        if error == 'UserNotFound':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')

        if error == 'NotVerified':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')

        if error == 'UserDeleted':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User disabled please contact support.')

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')

    return user_id
