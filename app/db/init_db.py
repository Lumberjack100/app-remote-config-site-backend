import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import create_user, get_user_by_account
from app.db.base import Base
from app.db.session import engine


def init_db(db: Session) -> None:
    """
    初始化数据库
    """
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建默认用户
    user = get_user_by_account(db, settings.DEFAULT_USER_ACCOUNT)
    if not user:
        create_user(
            db,
            account=settings.DEFAULT_USER_ACCOUNT,
            password=settings.DEFAULT_USER_PASSWORD,
            name=settings.DEFAULT_USER_NAME,
            company_id=settings.DEFAULT_USER_COMPANY_ID,
            company_name=settings.DEFAULT_USER_COMPANY_NAME,
        )
        logging.info("Created default user: %s", settings.DEFAULT_USER_ACCOUNT) 