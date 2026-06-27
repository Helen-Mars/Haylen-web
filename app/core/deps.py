from fastapi import Cookie, HTTPException, status
from sqlmodel import select

from app.core.security import verify_access_token
from app.db.session import SessionDep
from app.models.user import User


def get_current_user(
    db: SessionDep,
    access_token: str | None = Cookie(default=None),
) -> User:
    """Get the current authenticated user from the httpOnly cookie."""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or session expired",
        )

    # verify_access_token handles expired/invalid tokens internally (401)
    payload = verify_access_token(access_token)

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

