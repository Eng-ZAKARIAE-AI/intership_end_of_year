import os
import sys
from typing import List
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 1. Add 'backend' and 'couche_data' to python path
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
couche_data_dir = os.path.join(backend_dir, "couche_data")

for path in [base_dir, backend_dir, couche_data_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# 2. Import data layer components
from repositories.telemetry_repository import TelemetryRepository
from services.telemetry_service import TelemetryService
from controller.telemetry_controller import TelemetryController
from schemas.telemetry import TelemetryParsed

# 3. Path to SQLite database inside backend/system_event_loader
DB_PATH = os.path.abspath(os.path.join(backend_dir, "system_event_loader/telemetry_edge.db"))
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Initialize FastAPI App
app = FastAPI(
    title="Tech-IT Agent Telemetry API",
    description="API exposing edge device metrics, connected peripherals, and system logs",
    version="1.0.0"
)

# 5. Enable CORS for Frontend (React, Vue, Vite, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello from Tech-IT Agent API!"}

@app.get("/api/telemetry", response_model=List[TelemetryParsed])
def get_telemetry_records(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Fetches un-synced telemetry records."""
    repo = TelemetryRepository(db)
    service = TelemetryService(repo)
    controller = TelemetryController(service)
    
    return controller.get_agent_telemetry_context(limit=limit)

if __name__ == "__main__":
    import uvicorn
    print(f"🔗 Database connected at: {DB_PATH}")
    print("🚀 Starting Tech-IT Telemetry API server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)