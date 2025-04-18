from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

from app.db.base_class import Base


class SensorConfig(Base):
    """传感器配置表"""
    __tablename__ = "sensor_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    port = Column(String, nullable=False)  # 串口号: 485-1 或 485-2
    sensor_id = Column(Integer, nullable=False)  # 传感器ID
    sensor_name = Column(String, nullable=False)  # 传感器名称
    model_token = Column(String, nullable=False)  # 物模型编号
    model_name = Column(String, nullable=False)  # 物模型名称
    model_fields = Column(JSON, nullable=False)  # 物模型字段列表，JSON格式
    creator_id = Column(Integer, nullable=False)  # 创建者ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updater_id = Column(Integer, nullable=False)  # 更新者ID
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 更新时间 