from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.core.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """创建 JWT 登录令牌。"""

    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(token: str) -> dict:
    """验证 JWT 并返回 payload。"""

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )


def hash_password(password: str) -> str:
    """将明文密码转换为哈希。"""
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """验证明文密码是否匹配数据库中的哈希。"""
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )