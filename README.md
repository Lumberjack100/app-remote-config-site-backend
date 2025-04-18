# Android应用远程配置管理系统

这是一个专业、高效、易用的远程配置管理系统后端，帮助开发人员快速管理Android应用的配置参数。系统使用FastAPI框架实现。

## 功能特性

- 用户认证和鉴权
- MR702-遥测终端机传感器配置管理
  - 查询传感器配置列表
  - 添加传感器配置
  - 编辑传感器配置
  - 删除传感器配置

## 项目代码结构

```
app-remote-config-site-backend/
├── alembic/                 # 数据库迁移工具目录
│   ├── versions/            # 存放数据库迁移版本文件
│   └── env.py               # Alembic环境配置
├── app/                     # 主应用代码目录
│   ├── api/                 # API相关代码
│   │   └── v1/              # V1版本API
│   │       ├── endpoints/   # API端点
│   │       │   ├── auth.py  # 认证相关接口
│   │       │   └── config.py# 配置相关接口
│   │       └── api.py       # API路由配置
│   ├── core/                # 核心配置
│   │   ├── config.py        # 应用配置类
│   │   ├── security.py      # 安全相关工具函数
│   │   └── logging.py       # 日志配置
│   ├── crud/                # 数据库CRUD操作
│   │   ├── base.py          # 基础CRUD操作
│   │   ├── user.py          # 用户相关CRUD
│   │   └── config.py        # 配置相关CRUD
│   ├── db/                  # 数据库连接与初始化
│   │   ├── base.py          # 数据库基础设置
│   │   └── session.py       # 数据库会话管理
│   ├── middleware/          # 中间件
│   │   ├── cors.py          # CORS中间件
│   │   └── logging.py       # 日志中间件
│   ├── models/              # 数据库模型
│   │   ├── user.py          # 用户模型
│   │   └── config.py        # 配置模型
│   └── schemas/             # 请求和响应的Pydantic模型
│       ├── user.py          # 用户相关模型
│       └── config.py        # 配置相关模型
├── docs/                    # 文档
├── .env                     # 环境变量
├── .env.example             # 环境变量示例
├── alembic.ini              # Alembic配置文件
├── Dockerfile               # Docker构建文件
├── docker-compose.yml       # Docker Compose配置
├── main.py                  # 应用入口
└── requirements.txt         # Python依赖
```

### 主要文件说明

- **main.py**: 应用入口点，配置FastAPI应用，设置中间件和路由。这里初始化了FastAPI应用实例，注册中间件、路由和事件处理器，并启动应用。

- **app/api/v1/endpoints/**: 包含所有API端点的实现
  - **auth.py**: 用户认证相关接口，包括登录和获取用户信息。处理用户认证流程，生成和验证JWT令牌。
  - **config.py**: MR702传感器配置管理接口，提供查询、添加、编辑和删除传感器配置的功能。

- **app/models/**: 数据库ORM模型，定义数据结构
  - **user.py**: 定义用户模型，包含用户ID、账号、密码哈希等字段。
  - **config.py**: 定义MR702传感器配置模型，包含各种传感器参数和属性字段。

- **app/schemas/**: 请求和响应的数据验证模型
  - **user.py**: 包含用户相关的请求和响应模型，如登录请求、用户信息响应等。
  - **config.py**: 包含传感器配置相关的请求和响应模型，定义了配置项的各种参数和验证规则。

- **app/crud/**: 包含所有数据库CRUD操作的函数
  - **base.py**: 实现通用的CRUD操作基类，提供增删改查的基本功能。
  - **user.py**: 用户相关的CRUD操作，如验证用户，创建用户等。
  - **config.py**: 传感器配置相关的CRUD操作，包括查询、添加、编辑和批量删除配置项。

- **app/core/**: 核心配置，包括安全设置、配置加载等
  - **config.py**: 应用配置类，加载和管理环境变量和配置参数。
  - **security.py**: 安全工具函数，包括密码哈希、JWT令牌生成和验证等。
  - **logging.py**: 日志配置，设置日志级别、格式和输出方式。

- **app/middleware/**: 自定义中间件，如CORS和日志中间件
  - **cors.py**: CORS中间件配置，处理跨域请求。
  - **logging.py**: 日志中间件，记录请求和响应信息。

- **app/db/**: 数据库连接与初始化
  - **base.py**: 定义基础模型类和导入所有模型。
  - **session.py**: 数据库会话管理，创建数据库连接和会话。

- **docker-compose.yml**: 定义应用和数据库服务的Docker Compose配置，包括环境变量、端口映射和卷挂载等。

- **Dockerfile**: 定义Docker镜像构建过程，包括基础镜像、依赖安装和应用启动命令等。

- **alembic/**: 数据库迁移相关文件
  - **versions/**: 存放数据库迁移版本文件，记录数据库结构的变更历史。
  - **env.py**: Alembic环境配置，设置迁移环境的参数和上下文。

## 技术栈

- **FastAPI**: 高性能Python API框架，支持异步请求处理和自动API文档生成
- **SQLAlchemy**: Python ORM框架，提供对象关系映射功能
- **PostgreSQL**: 强大的开源关系型数据库系统
- **Pydantic**: 数据验证和设置管理库，用于请求和响应模型定义
- **JWT**: 用于用户认证的JSON Web Token实现
- **Docker & Docker Compose**: 容器化部署和编排工具

## 开发环境设置

### 方法一：直接在本地运行

1. **安装PostgreSQL数据库**（如果尚未安装）：
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. **创建数据库**：
   ```bash
   createdb remote_config
   ```

3. **复制环境配置**：
   ```bash
   cp .env.example .env
   ```

4. **安装Python依赖**：
   ```bash
   pip install -r requirements.txt
   ```

5. **运行数据库迁移**：
   ```bash
   alembic upgrade head
   ```

6. **运行应用**：
   ```bash
   uvicorn main:app --reload
   ```

### 方法二：使用Docker Compose（推荐）

1. **确保已安装Docker**：
   ```bash
   brew install docker docker-compose
   ```

2. **启动应用**：
   ```bash
   docker-compose up -d
   docker-compose up -d --build app
   ```

## 项目运行说明

### 使用Docker Compose启动（推荐）

**启动项目**:
```bash
# 在当前目录下，基于 docker-compose.yml 启动所有服务，并在后台运行，-d（--detach）表示"后台模式"（detached mode）
docker-compose up -d

# 重新构建并启动应用服务（如果镜像或配置更新）
docker-compose up -d --build app
```

**停止项目**:
```bash
# 停止所有服务
docker-compose down

# 停止并删除所有数据卷（会清除数据库数据）
docker-compose down -v
```

**查看项目日志**:
```bash
# 查看所有服务的日志
docker-compose logs

# 查看应用服务的日志
docker-compose logs app

# 实时查看应用服务的日志
docker-compose logs -f app
```

**查看项目运行状态**:
```bash
# 查看所有服务运行状态
docker-compose ps

# 查看容器详细信息
docker stats

# 查看容器资源使用情况
docker-compose top
```

**查看项目数据库**:
```bash
# 连接PostgreSQL数据库
docker-compose exec db psql -U postgres -d remote_config

# 数据库备份
docker-compose exec db pg_dump -U postgres remote_config > backup.sql

# 备份恢复
cat backup.sql | docker-compose exec -T db psql -U postgres -d remote_config
```


### 直接在本地运行

**本地启动**:
```bash
# 使用uvicorn启动并开启热重载
uvicorn main:app --reload

# 指定主机和端口
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 后台运行（使用nohup）
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

**本地停止**:
```bash
# 直接终止运行uvicorn的终端进程（Ctrl+C）

# 如果是后台运行，可以通过查找并终止进程
ps aux | grep uvicorn
kill <进程ID>
```

**查看项目日志**:
```bash
# 如果直接在终端运行，日志会输出到终端

# 如果使用nohup后台运行，查看日志文件
tail -f app.log

# 查看系统日志中的应用信息
journalctl -u app-remote-config.service (如果配置了systemd服务)
```

**查看项目运行状态**:
```bash
# 检查应用是否正在运行
lsof -i :8000

# 查看进程状态
ps aux | grep uvicorn

# 查看CPU和内存使用
top -p $(pgrep -f uvicorn)
```

**查看项目数据库**:
```bash
# 连接PostgreSQL数据库
psql -U postgres remote_config

# 执行SQL查询
psql -U postgres remote_config -c "SELECT * FROM users LIMIT 10;"

# 数据库备份
pg_dump -U postgres remote_config > backup.sql

# 备份恢复
psql -U postgres remote_config < backup.sql
```


### 查看项目配置

项目配置存储在以下文件中：
- **.env**: 环境变量配置文件
- **app/core/config.py**: 核心配置类
- **alembic.ini**: 数据库迁移配置

查看当前配置:
```bash
# 查看环境变量
cat .env

# Docker环境查看环境变量
docker-compose exec app cat .env

# 查看应用配置
cat app/core/config.py

# 查看数据库迁移配置
cat alembic.ini
```

### 数据库迁移操作

```bash
# 创建新的迁移版本（在修改模型后）
alembic revision --autogenerate -m "描述迁移内容"

# 应用所有迁移
alembic upgrade head

# 回滚到特定版本
alembic downgrade <版本号>

# Docker环境中执行迁移
docker-compose exec app alembic upgrade head
```

### 测试接口

应用启动后，可以通过以下方式测试接口：

1. **API文档**：访问 http://localhost:8000/docs 查看Swagger UI界面

2. **使用curl命令测试登录接口**：
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/SignIn" \
     -H "Content-Type: application/json" \
     -H "access_type: android" \
     -d '{"account": "medo_gh", "password": "medo123456"}'
   ```

## API文档

启动应用后，可以访问以下URL查看API文档:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 主要API端点

- 用户认证: `/api/v1/auth/SignIn`
- 获取用户信息: `/api/v1/auth/GetUserByToken`
- 查询传感器配置: `/api/v1/config/QueryMR702SensorConfigList`
- 添加传感器配置: `/api/v1/config/AddMR702SensorConfigItem`
- 编辑传感器配置: `/api/v1/config/EditMR702SensorConfigItem`
- 删除传感器配置: `/api/v1/config/BatchDeleteMR702SensorConfigItem`

