import os
from datetime import timedelta
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from jose import jwt
from sqlalchemy.orm import Session

from document_creation_task2.authentication import authenticate
from document_creation_task2.db.DAO.dao_user import UserDb
from document_creation_task2.db.dependencies import get_db_session as get_db
from document_creation_task2.db.models.users import RevokedToken, Token, UserDet
from document_creation_task2.services.user_service import (
    get_current_user,
    refresh_tok,
    token_gen,
)
from document_creation_task2.users.user_schema import User

users_func = APIRouter()
load_dotenv()
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


@users_func.post("/create_user")
def create_user(request: User, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """To create a new user.

    :param request:The user schema.
    :param db:The session of database
    :return: A dict containing the status of response
    """
    userdbs = UserDb()
    return userdbs.create_users(request, db)


@users_func.post("/user_login")
async def user_login(formdata: User, db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    To login for the user.

    :param formdata:Contains login name and password.
    :param db:The session db.
    :returns:The dict of tokens.

    :raises HTTPException: For unauthorized user.
    """
    mins = 30
    user = authenticate.authentic(formdata.name, formdata.password, db)
    if not isinstance(user, UserDet):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    flag = True
    refresh_token = refresh_tok(user.name, user.id, timedelta(minutes=mins), flag)
    tokens = token_gen(user.name, user.id, timedelta(minutes=mins))
    db.add(Token(accesstype=tokens, user_id=user.id))
    db.commit()
    return {"access_token": tokens, "refresh_token": refresh_token}


@users_func.post("/token/refresh")
async def refresh_access_token(
    refresh_token: str = Header(None),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Create a new access token based on a refresh token.

    :param refresh_token: The refresh token for authentication.
    :param db: The session db.

    :returns:A dictionary containing the new access token.
    :raises HTTPException: Raised for various authentication-related errors.
    """
    try:
        userid = get_current_user(refresh_token, db)
        payload = jwt.decode(refresh_token, secret_key, algorithms=algorithm)
        minute = 20
        if payload.get("ref_token"):
            username = payload.get("name")
            expiration = timedelta(minutes=minute)
            return {"access_token": token_gen(username, userid, expiration)}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid refresh token",
    )


@users_func.post("/user_signout")
async def user_signout(req: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    To sign out a user by invalidating the token and checking if it's revoked.

    :param req : The HTTP request object.
    :param db : Database session.
    :return:The message indicating that the user has been signed out.
    :raises HTTPException:- If the token is not provided in headers (status code 401)
    """
    token = req.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided in headers",
        )
    revoked_token = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    if revoked_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has already been revoked",
        )
    revoked_token = RevokedToken(token=token)
    db.add(revoked_token)
    db.commit()

    return {"message": "User has been signed out."}
