import json
from typing import List, Dict, Any
from couche_data.repositories.telemetry_repository import TelemetryRepository

class TelemetryService:
    def __init__(self, repository: TelemetryRepository):
        self.repository = repository

    def fetch_pending_telemetry(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les événements non synchronisés et parse le payload JSON."""
        records = self.repository.get_unsynced(limit=limit)
        parsed_records = []
        
        for record in records:
            try:
                payload_dict = json.loads(record.payload)
            except json.JSONDecodeError:
                payload_dict = {"raw": record.payload}

            parsed_records.append({
                "id": record.id,
                "timestamp": str(record.timestamp),
                "synced": record.synced,
                "data": payload_dict
            })
            
        return parsed_records