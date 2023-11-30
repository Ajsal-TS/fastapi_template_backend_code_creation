from typing import Any, Union

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from document_creation_task2.db.dependencies import get_db_session as get_db
from document_creation_task2.db.models.users import UserDet
from document_creation_task2.services.user_service import get_current_user

hashing = CryptContext(schemes=["bcrypt"])
api_key = APIKeyHeader(name="Authorization", auto_error=True)


def authentic(
    name: str,
    password: str,
    db: Session = Depends(get_db),
) -> Union[UserDet, bool]:
    """
    Validate username and password.

    :param name:Name of user
    :param password:password of user
    :param db:The session

    :returns:details of the valid user.
    """
    username = db.query(UserDet).filter(UserDet.name == name).first()

    if not username:
        return False
    data = hashing.verify(
        password,
        str(username.password),
    )
    if not data:
        return False
    return username


def token_authenticate(
    request: Request,
    token: Any = api_key,
    db: Session = Depends(get_db),
) -> str:
    """
    Authenticate the API key token and return the ID of the current user.

    :param request: FastAPI request object.
    :param token: Authorization token. Defaults to API key from headers.
    :param db: Database session. Defaults to Depends(get_db).

    :return: ID of the current user if authentication is successful.

    :raises HTTPException: If the token is not provided.
    """
    token_value = token
    if not token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return get_current_user(token_value, db)
