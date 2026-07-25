from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TelemetryBufferModel(Base):
    __tablename__ = "telemetry_buffer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, server_default=func.now())
    payload = Column(String, nullable=False)
    synced = Column(Integer, default=0)