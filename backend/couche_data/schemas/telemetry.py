from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# --- Sub-schemas for Payload Content ---

class CPUMetrics(BaseModel):
    usage_percent: float
    cores_logical: int
    load_avg_1min: float

class MemoryMetrics(BaseModel):
    total_gb: float
    used_percent: float
    available_gb: float

class SystemMetrics(BaseModel):
    hostname: str
    platform: str
    timestamp: datetime
    cpu: CPUMetrics
    memory: MemoryMetrics
    gpus: List[dict] = Field(default_factory=list)

class Peripherals(BaseModel):
    printers: List[str] = Field(default_factory=list)
    usb_devices: List[str] = Field(default_factory=list)

class SystemLogEntry(BaseModel):
    source_name: str
    timestamp: datetime
    priority: str
    message: str

class TelemetryPayload(BaseModel):
    """Structured representation of the raw JSON string in payload."""
    metrics: SystemMetrics
    peripherals: Peripherals
    logs: List[SystemLogEntry] = Field(default_factory=list)

# --- Main Database Schemas ---

class TelemetryRead(BaseModel):
    """Raw record directly from the database table."""
    id: int
    timestamp: Optional[datetime] = None
    payload: str
    synced: int

    class Config:
        from_attributes = True

class TelemetryParsed(BaseModel):
    """Full typed schema for consumption by services, controllers, and AI Agents."""
    id: int
    timestamp: Optional[datetime] = None
    payload_data: TelemetryPayload
    synced: int

    class Config:
        from_attributes = True