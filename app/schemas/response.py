from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class ResponseModel(GenericModel, Generic[T]):
    """
    通用响应模型
    """
    code: int = Field(0, description="错误码，0表示成功")
    msg: Optional[str] = Field(None, description="错误信息")
    data: Optional[T] = Field(None, description="响应数据") 