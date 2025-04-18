import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件，记录请求和响应信息
    """
    def __init__(self, app: FastAPI):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录请求信息
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else None,
            "process_time": f"{process_time:.3f}s",
            "status_code": response.status_code,
        }
        
        # 在实际应用中，可以使用logger记录
        print(request_info)
        
        return response 