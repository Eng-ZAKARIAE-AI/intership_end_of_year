from couche_data.services.telemetry_service import TelemetryService

class TelemetryController:
    def __init__(self, service: TelemetryService):
        self.service = service

    def get_agent_telemetry_context(self, limit: int = 5):
        """Fournit les métriques récentes sous forme de contexte pour l'Agent IA."""
        return self.service.fetch_pending_telemetry(limit=limit)