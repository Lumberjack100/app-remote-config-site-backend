#!/bin/bash

# 执行数据库迁移
echo "Running database migrations..."
alembic upgrade head

# 启动应用
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} 