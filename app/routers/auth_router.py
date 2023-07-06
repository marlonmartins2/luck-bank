from datetime import datetime, timedelta

from utils.logger import Logger

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services import oauth2
from services.oauth2 import AuthJWT
from services.password import Password

from settings import settings

from models.auth.login_model import LoginUserRequest

from database.controllers.user import (
    check_user_by_email,
    get_user_by_id,
    set_last_login,
)


logger = Logger.init("AuthRouterLogger")


auth_router = APIRouter(tags=["Auth"])
ACCESS_TOKEN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN = settings.REFRESH_TOKEN_EXPIRES_IN

@auth_router.post("/login/", status_code=status.HTTP_200_OK)
def login(payload: LoginUserRequest, Authorize: AuthJWT = Depends()):
    """
    Login user route.

    - **email**: the user email (EmailStr)
    - **password**: the user password(constr)

    Returns:
    - **Access Token**: the access token (str)
    - **Refresh Token**: the refresh token (str)
    """
    user = check_user_by_email(payload.email)

    if not Password.verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = Authorize.create_access_token(
        subject=user["id"],
        expires_time=timedelta(minutes=ACCESS_TOKEN),
    )

    refresh_token = Authorize.create_refresh_token(
        subject=user["id"],
        expires_time=timedelta(minutes=REFRESH_TOKEN),
    )

    set_last_login(user["id"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "message": "User logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        })
    )


@auth_router.post("/refresh/", status_code=status.HTTP_200_OK)
def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh access token."
            )

        user = get_user_by_id(user_id)

        access_token = Authorize.create_access_token(
            subject=user["id"],
            expires_time=timedelta(minutes=ACCESS_TOKEN),
        )

    except HTTPException as error:
        logger.error(f"Error refreshing token: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh access token."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "access_token": access_token,
            "token_type": "bearer",
        })
    )


@auth_router.post("/logout/", status_code=status.HTTP_200_OK)
def logout(Authorize: AuthJWT = Depends()):
    """
    Logout user route.

    - **Authorization**: the access token (str)

    Returns:
    - **Message**: the logout message (str)
    """
    try:
        Authorize.jwt_refresh_token_required()

        jti = Authorize.get_raw_jwt()["jti"]

        oauth2.denylist.add(jti)

    except HTTPException as error:
        logger.error(f"Error logging out user: {error}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not logout user."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "message": "User logged out successfully",
        })
    )
