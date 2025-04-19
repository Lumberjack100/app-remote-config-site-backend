# Android应用远程配置管理系统 - AWS Ubuntu Server 后端部署指南

## 目录

- [前置准备](#前置准备)
- [第一步：创建EC2实例](#第一步创建ec2实例)
- [第二步：连接到实例](#第二步连接到实例)
- [第三步：安装必要软件](#第三步安装必要软件)
- [第四步：安装配置PostgreSQL](#第四步安装配置postgresql)
- [第五步：部署后端应用](#第五步部署后端应用)
- [第六步：配置HTTPS（可选）](#第六步配置https可选)
- [第七步：备份策略](#第七步备份策略)
- [第八步：监控与维护](#第八步监控与维护)
- [故障排除](#故障排除)

## 前置准备

在开始部署之前，请确保满足以下条件：

1. 拥有AWS账号并且具备创建EC2实例的权限
2. 已准备好SSH密钥对用于连接EC2实例
3. 已将后端项目代码上传到GitHub或其他Git仓库
4. 了解基本的Linux命令和Docker操作

## 第一步：创建EC2实例

1. 登录AWS管理控制台
2. 导航到EC2服务
3. 点击"启动实例"按钮
4. 配置实例详情：
   - 名称：`remote-config-backend`
   - 应用程序和操作系统映像：选择"Ubuntu Server 22.04 LTS"
   - 实例类型：根据预算选择（建议至少t3.small）
   - 密钥对：选择或创建新的SSH密钥对
   - 网络设置：
     - 允许SSH流量（端口22）
     - 允许HTTP流量（端口80）
     - 允许HTTPS流量（端口443）
   - 配置存储：建议至少20GB（考虑到数据库存储需求）
5. 点击"启动实例"按钮

## 第二步：连接到实例

1. 等待实例状态变为"运行中"
2. 记录公共IPv4地址
3. 使用SSH连接到实例：

```bash
ssh -i your-key.pem ubuntu@your-instance-public-ip
```

## 第三步：安装必要软件

连接到实例后，执行以下命令安装必要的软件：

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装基本工具
sudo apt install -y git curl wget unzip

# 安装Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到docker组，避免每次都需要sudo
sudo usermod -aG docker ubuntu
newgrp docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

## 第四步：安装配置PostgreSQL

我们将使用Docker来运行PostgreSQL，这样可以更容易管理和备份：

```bash
# 创建项目目录
mkdir -p ~/app-remote-config
cd ~/app-remote-config

# 创建PostgreSQL数据目录
mkdir -p postgres-data

# 创建docker-compose文件
cat > docker-compose.yml << EOF
version: '3'

services:
  postgres:
    image: postgres:14
    container_name: postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=remote_config
      - POSTGRES_PASSWORD=strong_password_here  # 请修改为强密码
      - POSTGRES_DB=remote_config
    volumes:
      - ./postgres-data:/var/lib/postgresql/data

EOF

# 启动PostgreSQL容器
docker-compose up -d postgres

# 检查容器是否正常运行
docker ps
```

## 第五步：部署后端应用

### 克隆项目代码

```bash
# 进入项目目录
cd ~/app-remote-config

# 克隆后端代码
git clone https://github.com/your-username/app-remote-config-site-backend.git backend
cd backend
```

### 创建启动脚本

```bash
cat > start.sh << 'EOF'
#!/bin/bash

echo "Waiting for PostgreSQL..."
sleep 10

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
EOF

chmod +x start.sh
```

### 修改或确认Dockerfile

如果项目中已有Dockerfile，请确认它使用了start.sh脚本。如果没有，请创建：

```bash
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]
EOF
```

### 更新docker-compose.yml文件

```bash
cd ~/app-remote-config
cat > docker-compose.yml << 'EOF'
version: '3'

services:
  postgres:
    image: postgres:14
    container_name: postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=remote_config
      - POSTGRES_PASSWORD=strong_password_here  # 请修改为强密码
      - POSTGRES_DB=remote_config
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    
  api:
    build: ./backend
    container_name: api
    restart: always
    depends_on:
      - postgres
    ports:
      - "80:8000"
    environment:
      - DATABASE_URL=postgresql://remote_config:strong_password_here@postgres:5432/remote_config  # 请保持密码一致
      - SECRET_KEY=your_secure_secret_key_at_least_32_characters  # 使用安全密钥
      - ENVIRONMENT=production
      - ALLOWED_HOSTS=*,your-instance-public-ip
      - ACCESS_TOKEN_EXPIRE_MINUTES=43200
      - CORS_ORIGINS=*
EOF
```

### 构建并启动应用

```bash
# 构建并启动所有服务
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看API容器日志
docker logs api
```

## 第六步：配置HTTPS（可选）

如果你有域名并希望使用HTTPS，可以按照以下步骤配置Nginx和Let's Encrypt：

```bash
# 安装Nginx和Certbot
sudo apt install -y nginx certbot python3-certbot-nginx

# 创建Nginx配置文件
sudo cat > /etc/nginx/sites-available/remote-config << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/remote-config /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com  # 替换为您的域名

# 配置自动续期
sudo systemctl status certbot.timer
```

## 第七步：备份策略

### 创建备份脚本

```bash
cd ~/app-remote-config
cat > backup.sh << 'EOF'
#!/bin/bash

# 设置变量
BACKUP_DIR=~/backups
DATE=$(date +%Y-%m-%d_%H-%M-%S)
DB_CONTAINER=postgres
DB_USER=remote_config
DB_NAME=remote_config

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
echo "Creating database backup..."
docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/db_backup_$DATE.sql

# 只保留最近7天的备份
echo "Cleaning old backups..."
find $BACKUP_DIR -name "db_backup_*.sql.gz" -type f -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.sql.gz"
EOF

chmod +x backup.sh

# 测试备份脚本
./backup.sh
```

### 设置定时备份

```bash
# 编辑crontab
crontab -e

# 添加以下行以每天凌晨2点执行备份
0 2 * * * ~/app-remote-config/backup.sh
```

## 第八步：监控与维护

### 设置基本监控

```bash
# 安装监控工具
sudo apt install -y htop iotop

# 监控磁盘空间
cat > ~/check_disk.sh << 'EOF'
#!/bin/bash

THRESHOLD=80
USAGE=$(df -h / | grep / | awk '{print $5}' | sed 's/%//')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
  echo "Warning: Disk usage is at $USAGE%"
fi
EOF

chmod +x ~/check_disk.sh

# 添加到crontab
crontab -e

# 添加以下行以每天检查磁盘空间
0 9 * * * ~/check_disk.sh
```

### 日志轮转

```bash
# 创建日志轮转配置
sudo cat > /etc/logrotate.d/docker << 'EOF'
/var/lib/docker/containers/*/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    copytruncate
}
EOF
```

### 自动更新

```bash
# 创建自动更新脚本
cat > ~/update.sh << 'EOF'
#!/bin/bash

# 更新系统包
sudo apt update && sudo apt upgrade -y

# 清理不需要的包
sudo apt autoremove -y

# 重启Docker服务
sudo systemctl restart docker
EOF

chmod +x ~/update.sh

# 添加到crontab，每周日凌晨3点执行
crontab -e

# 添加以下行
0 3 * * 0 ~/update.sh
```

## 故障排除

### 应用无法启动

1. 检查容器状态:
```bash
docker ps -a
```

2. 查看容器日志:
```bash
docker logs api
```

3. 检查环境变量是否设置正确:
```bash
docker-compose config
```

### 数据库连接问题

1. 确认PostgreSQL容器正在运行:
```bash
docker ps | grep postgres
```

2. 检查数据库连接:
```bash
docker exec -it postgres psql -U remote_config -d remote_config -c "SELECT 1;"
```

3. 验证连接URL格式是否正确:
```bash
echo $DATABASE_URL
# 应为: postgresql://remote_config:password@postgres:5432/remote_config
```

### 系统资源不足

1. 检查系统资源使用情况:
```bash
htop
```

2. 检查磁盘空间:
```bash
df -h
```

3. 如果资源不足，考虑升级EC2实例类型或清理不必要的文件。

### HTTPS配置问题

1. 检查Nginx配置:
```bash
sudo nginx -t
```

2. 查看Nginx错误日志:
```bash
sudo tail -f /var/log/nginx/error.log
```

3. 重新申请SSL证书:
```bash
sudo certbot --nginx -d your-domain.com
``` 