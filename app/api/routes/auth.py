from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlmodel import select

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.deps import get_current_user


from app.db.session import SessionDep
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings

router = APIRouter(prefix="/authing")



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {"message": "Logged out successfully"}


@router.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user)):
    if current_user.username == "admin":
        return {"message": "Welcome, Admin!", "role": "admin"}
    return {"message": "Welcome, User!", "role": "user"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    }


@router.post("/login")
async def login(user: UserLogin, response: Response, db: SessionDep):
    statement = select(User).where(User.username == user.username)
    user_db = db.exec(statement).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(data={"sub": user_db.username})

    # 勾选 Remember me → 30 天，否则用配置的默认过期时间
    cookie_max_age = (
        30 * 24 * 60 * 60  # 30 days
        if user.remember_me
        else settings.access_token_expire_minutes * 60
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=cookie_max_age,
        path="/",
    )

    return {
        "user": {
            "id": user_db.id,
            "username": user_db.username,
            "email": user_db.email,
        }
    }


@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, session: SessionDep):
    # 检查用户名是否已存在
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # 检查邮箱是否已存在
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_dict = user.model_dump()
    user_dict["hashed_password"] = hash_password(user.password)
    db_user = User.model_validate(user_dict)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

