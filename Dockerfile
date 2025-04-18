FROM docker.io/library/python:3.10-slim

WORKDIR /app

# 复制项目文件
COPY ./requirements.txt /app/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 复制代码
COPY . /app/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
