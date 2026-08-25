import os

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Detection
from routes.services.ai_service import detect_plastic


router = APIRouter(
    prefix="/detection",
    tags=["Detection"]
)


@router.post("/detect")
async def detect(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    if file.content_type not in allowed_types:
        return {
            "success": False,
            "message": "Only JPG and PNG images are allowed"
        }

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Send image to AI service
    ai_result = detect_plastic(file_path)

    object_name = ai_result["object_name"]
    confidence = ai_result["confidence"]

    # Save result to database
    detection = Detection(
        image_name=file.filename,
        object_name=object_name,
        confidence=confidence
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)

    return {
        "success": True,
        "message": "Detection completed",
        "result": {
            "id": detection.id,
            "image_name": detection.image_name,
            "object_name": detection.object_name,
            "confidence": detection.confidence
        }
    }


@router.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    detections = (
        db.query(Detection)
        .order_by(Detection.id.desc())
        .all()
    )

    return {
        "success": True,
        "count": len(detections),
        "data": [
            {
                "id": detection.id,
                "image_name": detection.image_name,
                "object_name": detection.object_name,
                "confidence": detection.confidence,
                "detected_at": detection.detected_at
            }
            for detection in detections
        ]
    }