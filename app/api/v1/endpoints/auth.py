from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.crud.user import authenticate_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.response import ResponseModel
from app.schemas.user import Token, UserLogin, UserResponse, UserInDB

router = APIRouter()


@router.post("/SignIn", response_model=ResponseModel[str])
def login_access_token(
    user_login: UserLogin,
    db: Session = Depends(get_db),
    access_type: str = Header(None)
) -> Any:
    """
    用户登录接口
    """
    # TODO: 后续可以根据access_type适配不同的客户端
    
    user = authenticate_user(db, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 构建token附加数据
    extra_data = {
        "companyID": str(user.company_id),
        "subjectType": "0",  # 默认为用户类型
        "subjectName": user.name
    }
    
    token = create_access_token(
        user.id, expires_delta=access_token_expires, extra_data=extra_data
    )
    
    return ResponseModel[str](data=token)


@router.get("/GetUserByToken", response_model=ResponseModel[UserResponse])
def get_user_by_token(
    current_user: UserInDB = Depends(get_current_user),
) -> Any:
    """
    通过Token获取用户信息
    """
    return ResponseModel[UserResponse](
        data=UserResponse(
            subjectID=current_user.id,
            subjectName=current_user.name,
            companyID=current_user.company_id,
            companyName=current_user.company_name
        )
    ) 