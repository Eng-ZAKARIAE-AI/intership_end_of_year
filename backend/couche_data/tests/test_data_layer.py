import os
import sys

# 1. Configuration des chemins pour résoudre tous les imports (couche_data et backend)
base_dir = os.path.dirname(os.path.abspath(__file__))
couche_data_dir = os.path.abspath(os.path.join(base_dir, ".."))
backend_dir = os.path.abspath(os.path.join(base_dir, "../.."))

for path in [couche_data_dir, backend_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 2. Importation des composants de la couche data
from models.telemetry import Base, TelemetryBufferModel
from repositories.telemetry_repository import TelemetryRepository
from services.telemetry_service import TelemetryService
from controller.telemetry_controller import TelemetryController

# 3. Chemin absolu vers la base SQLite
DB_PATH = os.path.abspath(os.path.join(base_dir, "../../system_event_loader/telemetry_edge.db"))
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"Connexion à la base de données : {DATABASE_URL}")

# 4. Initialisation de la session SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_test():
    db = SessionLocal()
    try:
        # Initialisation de la chaîne de dépendances
        repo = TelemetryRepository(db)
        service = TelemetryService(repo)
        controller = TelemetryController(service)

        print("\n--- TEST : Récupération complète des télémétries ---")
        context_data = controller.get_agent_telemetry_context(limit=5)
        
        print(f"Nombre d'enregistrements récupérés : {len(context_data)}")
        
        for record in context_data:
            print("\n==================================================")
            print(f" Record ID : {record.id}")
            print(f" Timestamp : {record.timestamp}")
            print(f" Synced    : {record.synced}")
            print("==================================================")
            
            payload = record.payload_data
            
            # --- Métriques Système ---
            metrics = payload.metrics
            print("\n 💻 [MÉTRIQUES SYSTÈME]")
            print(f"   • Hostname     : {metrics.hostname}")
            print(f"   • Plateforme   : {metrics.platform}")
            print(f"   • Usage CPU    : {metrics.cpu.usage_percent}% ({metrics.cpu.cores_logical} cœurs, Load Avg 1m: {metrics.cpu.load_avg_1min})")
            print(f"   • Usage RAM    : {metrics.memory.used_percent}% ({metrics.memory.available_gb} GB dispo / {metrics.memory.total_gb} GB total)")
            print(f"   • GPUs         : {metrics.gpus if metrics.gpus else 'Aucun détecté'}")

            # --- Périphériques Connectés ---
            peripherals = payload.peripherals
            print("\n 🔌 [PÉRIPHÉRIQUES CONNECTÉS]")
            print(f"   • Appareils USB ({len(peripherals.usb_devices)}) :")
            if peripherals.usb_devices:
                for usb in peripherals.usb_devices:
                    print(f"       - {usb}")
            else:
                print("       - Aucun appareil USB détecté")

            print(f"   • Imprimantes ({len(peripherals.printers)}) :")
            if peripherals.printers:
                for printer in peripherals.printers:
                    print(f"       - {printer}")
            else:
                print("       - Aucune imprimante détectée")

            # --- Journaux Système ---
            logs = payload.logs
            print(f"\n 📜 [LOGS SYSTÈME] ({len(logs)} entrées)")
            for log in logs[:3]:  # Affiche les 3 premiers logs en aperçu
                print(f"   • [{log.source_name} | Priorité {log.priority}] {log.message}")
            if len(logs) > 3:
                print(f"     ... et {len(logs) - 3} autres entrées de log.")

    except Exception as e:
        print(f" ❌ Erreur lors du test : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()