from fastapi import FastAPI

from database import engine, Base
from routes.detection import router as detection_router
import models


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Plastic Waste Detection API",
    description="Backend API for plastic waste detection",
    version="1.0.0"
)


app.include_router(detection_router)


@app.get("/")
def home():
    return {
        "message": "Plastic Waste Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }