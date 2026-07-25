from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

# Schéma pour lire un enregistrement depuis la BDD
class TelemetryRead(BaseModel):
    id: int
    timestamp: Optional[datetime] = None
    payload: str
    synced: int

    class Config:
        from_attributes = True

# Schéma parsé (payload décomposé en dictionnaire pour l'Agent IA)
class TelemetryParsed(BaseModel):
    id: int
    timestamp: Optional[datetime] = None
    payload_data: Dict[str, Any]
    synced: int