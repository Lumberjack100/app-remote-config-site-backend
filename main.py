import logging

import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.middleware.cors import setup_cors_middleware
from app.middleware.logging import LoggingMiddleware

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Android应用远程配置管理系统",
    description="为Android应用提供远程配置管理功能",
    version="1.0.0",
)

# 设置CORS中间件
setup_cors_middleware(app)

# 添加日志中间件
app.add_middleware(LoggingMiddleware)

# 认证错误处理
@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"认证失败: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "msg": "认证失败，请检查token格式是否正确或重新登录",
            "data": None
        },
    )

# 权限错误处理
@app.exception_handler(status.HTTP_403_FORBIDDEN)
async def forbidden_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"权限不足: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "msg": "权限不足，无法访问该资源",
            "data": None
        },
    )

# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": "内部服务器错误",
            "data": None
        },
    )

# 添加API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 初始化数据库
@app.on_event("startup")
def startup_event():
    try:
        db: Session = SessionLocal()
        init_db(db)
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
