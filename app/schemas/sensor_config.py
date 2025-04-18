from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ModelField(BaseModel):
    """
    物模型字段模型
    """
    fieldName: str
    engUnit: str
    hydrologicalIdentification: str
    collectionInstructions: str
    ratio: str
    dataFormat: str
    triggerValue: str
    upperLimit: str
    lowerLimit: str
    correctValue: str
    ngateval: str


class SensorConfigCreate(BaseModel):
    """
    创建传感器配置请求模型
    """
    port: str
    sensorID: int
    sensorName: str
    modelToken: str
    modelName: str
    modelFieldList: List[ModelField]


class SensorConfigUpdate(BaseModel):
    """
    更新传感器配置请求模型
    """
    id: int
    port: str
    sensorID: int
    sensorName: str
    modelToken: str
    modelName: str
    modelFieldList: List[ModelField]


class SensorConfigInDB(SensorConfigCreate):
    """
    数据库中的传感器配置模型
    """
    id: int
    createUserID: int
    createTime: datetime
    updateUserID: int
    updateTime: datetime


class SensorConfigQuery(BaseModel):
    """
    查询传感器配置请求模型
    """
    port: Optional[str] = None
    sensorName: Optional[str] = None


class SensorConfigDeleteRequest(BaseModel):
    """
    删除传感器配置请求模型
    """
    ids: List[int]


class SensorConfigResponse(BaseModel):
    """
    传感器配置响应模型
    """
    sensorList: List[SensorConfigInDB]


class SensorConfigCreateResponse(BaseModel):
    """
    创建传感器配置响应模型
    """
    id: int 