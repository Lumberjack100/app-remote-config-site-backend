from typing import Generator, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import get_user_by_id
from app.db.session import get_db
from app.schemas.user import UserInDB

class CustomHTTPBearer(HTTPBearer):
    """
    自定义HTTPBearer认证类，允许直接使用token而不需要Bearer前缀
    """
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            # 尝试标准的Bearer认证
            return await super().__call__(request)
        except HTTPException as exc:
            # 如果标准认证失败，尝试直接从头部获取token
            auth_header = request.headers.get("Authorization")
            if auth_header:
                # 直接使用头部值作为token
                return HTTPAuthorizationCredentials(credentials=auth_header, scheme="")
            # 如果没有任何认证信息，则抛出原始异常
            raise exc

# 使用自定义的Bearer认证
security = CustomHTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserInDB:
    """
    获取当前用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        # 如果token以"Bearer "开头，则去掉前缀
        if token.startswith("Bearer "):
            token = token[7:]
            
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return UserInDB.model_validate(
        {
            "id": user.id,
            "account": user.account,
            "name": user.name,
            "company_id": user.company_id,
            "company_name": user.company_name,
        }
    ) 