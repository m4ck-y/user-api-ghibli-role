from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.infrastructure.config.settings import settings
from app.domain.schemas.auth import TokenData


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        role_name: str = payload.get("role_name")
        if user_id is None or role_name is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, role_name=role_name)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data