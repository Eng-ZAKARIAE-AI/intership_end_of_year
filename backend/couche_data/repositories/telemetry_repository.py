from sqlalchemy.orm import Session
from models.telemetry import TelemetryBufferModel
from typing import List

class TelemetryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_unsynced(self, limit: int = 10) -> List[TelemetryBufferModel]:
        """Récupère les enregistrements non synchronisés (synced = 0)"""
        return self.db.query(TelemetryBufferModel)\
                      .filter(TelemetryBufferModel.synced == 0)\
                      .order_by(TelemetryBufferModel.timestamp.asc())\
                      .limit(limit)\
                      .all()

    def mark_as_synced(self, record_ids: List[int]) -> int:
        """Marque une liste d'IDs comme synchronisés (synced = 1)"""
        updated = self.db.query(TelemetryBufferModel)\
                         .filter(TelemetryBufferModel.id.in_(record_ids))\
                         .update({"synced": 1}, synchronize_session=False)
        self.db.commit()
        return updated