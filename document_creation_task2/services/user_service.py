import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import JWTError, jwt

from document_creation_task2.db.DAO.dao_user import UserDb

load_dotenv()
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")


def refresh_tok(name: Any, ids: Any, time: Any, refresh: bool) -> str:
    """
    Generate and return a refresh token.

    :param name:Name of the user.
    :param ids:ID of the user.
    :param time:Access token active time.
    :param refresh: The status of the refresh token.

    :returns:The generated refresh token.
    """
    payload = {"id": ids, "name": name, "ref_token": refresh}
    expiration = datetime.utcnow() + time
    payload["expiration"] = expiration.isoformat()
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def token_gen(name: Any, ids: Any, time: Any) -> str:
    """Generate and returns the access token.

    :param name:name of the user.
    :param ids:id of the user.
    :param time: accesstoken active time.
    :returns:access token.
    """
    payload = {"name": name, "id": ids}
    expiration = datetime.utcnow() + time
    payload["expiration"] = expiration.isoformat()
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def get_current_user(token: Any, db: Any) -> str:
    """Returns the user id of the current active user.

    :param token: The token of the current user.
    :param db: The session.

    :returns: User ID of the current active user.
    :raises HTTPException: Unauthorized user, token revoked, or expired.
    """
    try:
        UserDb().revoked_token(token, db)
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        expiration = datetime.fromisoformat(payload["expiration"])

        if datetime.utcnow() > expiration:
            error_det = "Token has expired"
        else:
            user_id: str = payload.get("id")
            if user_id is None:
                error_det = "User ID not found in token"
            else:
                return user_id

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_det)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
