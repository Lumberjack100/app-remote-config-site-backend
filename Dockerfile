FROM docker.io/library/python:3.10-slim

WORKDIR /app

# 复制项目文件
COPY ./requirements.txt /app/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 复制代码
COPY . /app/

# 确保启动脚本有执行权限
RUN chmod +x /app/start.sh

# 暴露端口
EXPOSE 8000

# 使用启动脚本
CMD ["/app/start.sh"]
