from typing import Any, Dict

from fastapi import HTTPException, status
from passlib.context import CryptContext

from document_creation_task2.db.models.users import RevokedToken, UserDet

hashing = CryptContext(schemes=["bcrypt"])


class UserDb:
    """Class for user database methods."""

    def create_users(self, request: Any, db: Any) -> Dict[str, Any]:
        """Create user account.

        :param request:The user details.
        :param db:The session.
        :returns:The response status.
        :raises HTTPException:Not created.
        """
        try:
            new_user = UserDet(
                name=request.name,
                password=hashing.hash(request.password),
            )
            db.add(new_user)
            db.commit()
            return {
                "status": "success",
                "message": "successfully created a new user",
                "data": [],
                "error": False,
            }
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Not Created",
            )

    def revoked_token(self, token: Any, db: Any) -> None:
        """
         To find the user id of current active user.

        :param token: The token of the current user.

        :param db:The session db.

        :raises HTTPException: Unauthorized User.
        """
        revoked_token = (
            db.query(RevokedToken).filter(RevokedToken.token == token).first()
        )
        if revoked_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )
