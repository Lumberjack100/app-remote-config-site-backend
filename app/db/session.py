from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 将PostgreSQL URL转换为字符串格式
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    获取数据库会话依赖
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 