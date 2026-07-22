from fastapi import FastAPI

app = FastAPI(
    title="IT Maintenance RAG Platform API",
    version="1.0.0",
    description="Backend API for real-time monitoring, anomaly detection, and RAG assistant."
)

@app.get("/health")
def health_check():
    return {"status": "online", "system": "RAG IT Maintenance API"}
