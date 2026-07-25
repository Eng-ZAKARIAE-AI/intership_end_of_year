import sys
import os

# 1. Add the parent directory ('couche_data') to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2. Imports will now resolve correctly
from models.telemetry import Base, TelemetryBufferModel
from repositories.telemetry_repository import TelemetryRepository
from services.telemetry_service import TelemetryService
from controller.telemetry_controller import TelemetryController

# 3. Path to SQLite database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../system_event_loader/telemetry_edge.db"))
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"Connexion à la base de données : {DATABASE_URL}")

# 4. Initialisation SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_test():
    db = SessionLocal()
    try:
        repo = TelemetryRepository(db)
        service = TelemetryService(repo)
        controller = TelemetryController(service)

        print("\n--- TEST : Récupération des télémétries ---")
        context_data = controller.get_agent_telemetry_context(limit=5)
        print(f"Nombre d'enregistrements : {len(context_data)}")
        
        for record in context_data:
            print("----------------------------------------")
            print(f" ID        : {record['id']}")
            print(f" Timestamp : {record['timestamp']}")
            print(f" Synced    : {record['synced']}")
            
            metrics = record['data'].get('metrics', {})
            cpu = metrics.get('cpu', {})
            memory = metrics.get('memory', {})
            
            print(f" Hostname  : {metrics.get('hostname')}")
            print(f" CPU Usage : {cpu.get('usage_percent')}%")
            print(f" RAM Usage : {memory.get('used_percent')}%\n")

    except Exception as e:
        print(f" Erreur lors du test : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()