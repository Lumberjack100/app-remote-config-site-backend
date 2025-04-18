from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.sensor_config import SensorConfig
from app.schemas.sensor_config import SensorConfigCreate, SensorConfigUpdate


def create_sensor_config(
    db: Session, *, sensor_config: SensorConfigCreate, creator_id: int
) -> SensorConfig:
    """
    创建传感器配置
    """
    db_sensor_config = SensorConfig(
        port=sensor_config.port,
        sensor_id=sensor_config.sensorID,
        sensor_name=sensor_config.sensorName,
        model_token=sensor_config.modelToken,
        model_name=sensor_config.modelName,
        model_fields=[field.model_dump() for field in sensor_config.modelFieldList],
        creator_id=creator_id,
        updater_id=creator_id,
    )
    db.add(db_sensor_config)
    db.commit()
    db.refresh(db_sensor_config)
    return db_sensor_config


def get_sensor_configs(
    db: Session, *, port: Optional[str] = None, sensor_name: Optional[str] = None
) -> List[SensorConfig]:
    """
    获取传感器配置列表
    """
    query = db.query(SensorConfig)
    if port:
        query = query.filter(SensorConfig.port == port)
    if sensor_name:
        query = query.filter(SensorConfig.sensor_name.ilike(f"%{sensor_name}%"))
    return query.all()


def get_sensor_config_by_id(db: Session, sensor_config_id: int) -> Optional[SensorConfig]:
    """
    通过ID获取传感器配置
    """
    return db.query(SensorConfig).filter(SensorConfig.id == sensor_config_id).first()


def update_sensor_config(
    db: Session, *, db_sensor_config: SensorConfig, sensor_config: SensorConfigUpdate, updater_id: int
) -> SensorConfig:
    """
    更新传感器配置
    """
    update_data = sensor_config.model_dump(exclude={"id"})
    
    # 将驼峰命名转为下划线命名
    db_sensor_config.port = update_data["port"]
    db_sensor_config.sensor_id = update_data["sensorID"]
    db_sensor_config.sensor_name = update_data["sensorName"]
    db_sensor_config.model_token = update_data["modelToken"]
    db_sensor_config.model_name = update_data["modelName"]
    db_sensor_config.model_fields = [field.model_dump() for field in sensor_config.modelFieldList]
    db_sensor_config.updater_id = updater_id
    
    db.add(db_sensor_config)
    db.commit()
    db.refresh(db_sensor_config)
    return db_sensor_config


def delete_sensor_configs(db: Session, *, ids: List[int]) -> None:
    """
    删除传感器配置
    """
    db.query(SensorConfig).filter(SensorConfig.id.in_(ids)).delete(synchronize_session=False)
    db.commit()


def check_sensor_id_exists(db: Session, *, port: str, sensor_id: int, exclude_id: Optional[int] = None) -> bool:
    """
    检查传感器ID在同一串口下是否已存在
    """
    query = db.query(SensorConfig).filter(
        and_(
            SensorConfig.port == port,
            SensorConfig.sensor_id == sensor_id
        )
    )
    
    if exclude_id:
        query = query.filter(SensorConfig.id != exclude_id)
    
    return db.query(query.exists()).scalar() 