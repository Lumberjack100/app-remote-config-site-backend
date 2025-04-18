from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserLogin


def create_user(
    db: Session,
    *,
    account: str,
    password: str,
    name: str,
    company_id: int,
    company_name: str,
) -> User:
    """
    创建用户
    """
    hashed_password = get_password_hash(password)
    db_user = User(
        account=account,
        password=hashed_password,
        name=name,
        company_id=company_id,
        company_name=company_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_account(db: Session, account: str) -> Optional[User]:
    """
    通过账号获取用户
    """
    return db.query(User).filter(User.account == account).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    通过ID获取用户
    """
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, user_login: UserLogin) -> Optional[User]:
    """
    验证用户
    """
    user = get_user_by_account(db, user_login.account)
    if user and verify_password(user_login.password, user.password):
        return user
    return None 