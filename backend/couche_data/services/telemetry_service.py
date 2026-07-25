import json
from typing import List
from repositories.telemetry_repository import TelemetryRepository
from schemas.telemetry import TelemetryParsed, TelemetryPayload

class TelemetryService:
    def __init__(self, repository: TelemetryRepository):
        self.repository = repository

    def fetch_pending_telemetry(self, limit: int = 10) -> List[TelemetryParsed]:
        records = self.repository.get_unsynced(limit=limit)
        parsed_records = []
        
        for record in records:
            payload_dict = json.loads(record.payload)
            
            # Validates and maps the raw JSON directly into Pydantic models
            structured_payload = TelemetryPayload(**payload_dict)
            
            parsed_records.append(
                TelemetryParsed(
                    id=record.id,
                    timestamp=record.timestamp,
                    synced=record.synced,
                    payload_data=structured_payload
                )
            )
            
        return parsed_records