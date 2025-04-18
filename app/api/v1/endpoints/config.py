from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.crud.sensor_config import (check_sensor_id_exists, create_sensor_config,
                               delete_sensor_configs, get_sensor_config_by_id,
                               get_sensor_configs, update_sensor_config)
from app.db.session import get_db
from app.models.sensor_config import SensorConfig
from app.schemas.response import ResponseModel
from app.schemas.sensor_config import (SensorConfigCreate, SensorConfigCreateResponse,
                                  SensorConfigDeleteRequest, SensorConfigInDB,
                                  SensorConfigQuery, SensorConfigResponse,
                                  SensorConfigUpdate)
from app.schemas.user import UserInDB

router = APIRouter()


def convert_to_response_model(sensor_config: SensorConfig) -> SensorConfigInDB:
    """
    将数据库模型转换为响应模型
    """
    return SensorConfigInDB(
        id=sensor_config.id,
        port=sensor_config.port,
        sensorID=sensor_config.sensor_id,
        sensorName=sensor_config.sensor_name,
        modelToken=sensor_config.model_token,
        modelName=sensor_config.model_name,
        modelFieldList=sensor_config.model_fields,
        createUserID=sensor_config.creator_id,
        createTime=sensor_config.created_at,
        updateUserID=sensor_config.updater_id,
        updateTime=sensor_config.updated_at
    )


@router.post("/QueryMR702SensorConfigList", response_model=ResponseModel[SensorConfigResponse])
def query_mr702_sensor_config_list(
    query: SensorConfigQuery,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    获取MR702-遥测终端机传感器配置列表
    """
    sensor_configs = get_sensor_configs(
        db, port=query.port, sensor_name=query.sensorName
    )
    
    response_sensor_configs = [
        convert_to_response_model(sensor_config)
        for sensor_config in sensor_configs
    ]
    
    return ResponseModel[SensorConfigResponse](
        data=SensorConfigResponse(sensorList=response_sensor_configs)
    )


@router.post("/AddMR702SensorConfigItem", response_model=ResponseModel[SensorConfigCreateResponse])
def add_mr702_sensor_config_item(
    sensor_config: SensorConfigCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    添加MR702-遥测终端机传感器配置项
    """
    # 验证传感器ID在同一串口下是否唯一
    if check_sensor_id_exists(db, port=sensor_config.port, sensor_id=sensor_config.sensorID):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"传感器ID {sensor_config.sensorID} 在串口 {sensor_config.port} 下已存在"
        )
    
    # 创建传感器配置
    db_sensor_config = create_sensor_config(
        db, sensor_config=sensor_config, creator_id=current_user.id
    )
    
    return ResponseModel[SensorConfigCreateResponse](
        code=200,
        msg="success",
        data=SensorConfigCreateResponse(id=db_sensor_config.id)
    )


@router.post("/EditMR702SensorConfigItem", response_model=ResponseModel[None])
def edit_mr702_sensor_config_item(
    sensor_config: SensorConfigUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    编辑MR702-遥测终端机传感器配置项
    """
    # 验证传感器配置是否存在
    db_sensor_config = get_sensor_config_by_id(db, sensor_config.id)
    if not db_sensor_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"传感器配置 ID {sensor_config.id} 不存在"
        )
    
    # 验证传感器ID在同一串口下是否唯一
    if check_sensor_id_exists(
        db, 
        port=sensor_config.port, 
        sensor_id=sensor_config.sensorID,
        exclude_id=sensor_config.id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"传感器ID {sensor_config.sensorID} 在串口 {sensor_config.port} 下已存在"
        )
    
    # 更新传感器配置
    update_sensor_config(
        db, 
        db_sensor_config=db_sensor_config, 
        sensor_config=sensor_config,
        updater_id=current_user.id
    )
    
    return ResponseModel[None](
        code=200,
        msg="success",
        data=None
    )


@router.post("/BatchDeleteMR702SensorConfigItem", response_model=ResponseModel[None])
def batch_delete_mr702_sensor_config_item(
    delete_request: SensorConfigDeleteRequest,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
) -> Any:
    """
    批量删除MR702-遥测终端机传感器配置项
    """
    # 删除传感器配置
    delete_sensor_configs(db, ids=delete_request.ids)
    
    return ResponseModel[None](
        code=200,
        msg="success",
        data=None
    ) 