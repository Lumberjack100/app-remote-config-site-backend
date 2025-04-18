from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """
    用户登录请求模型
    """
    account: str
    password: str


class UserInDB(BaseModel):
    """
    数据库中的用户模型
    """
    id: int
    account: str
    name: str
    company_id: int
    company_name: str


class UserResponse(BaseModel):
    """
    用户信息响应模型
    """
    subjectID: int = Field(..., description="用户ID")
    subjectName: str = Field(..., description="用户名称")
    companyID: int = Field(..., description="公司ID")
    companyName: str = Field(..., description="公司名称")


class Token(BaseModel):
    """
    Token响应模型
    """
    access_token: str 