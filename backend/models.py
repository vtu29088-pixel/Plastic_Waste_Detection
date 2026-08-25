from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)

    image_name = Column(String)
    object_name = Column(String)

    confidence = Column(Float)

    detected_at = Column(
        DateTime,
        default=datetime.utcnow
    )