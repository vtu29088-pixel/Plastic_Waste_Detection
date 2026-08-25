from ultralytics import YOLO
import os

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "best.pt"
)

model = YOLO(MODEL_PATH)


def detect_plastic(image_path):
    results = model(image_path, conf=0.25)

    if not results or len(results[0].boxes) == 0:
        return {
            "object_name": "Unknown",
            "confidence": 0.0
        }

    result = results[0]

    # Get the detection with highest confidence
    best_index = result.boxes.conf.argmax().item()

    class_id = int(result.boxes.cls[best_index].item())
    confidence = float(result.boxes.conf[best_index].item())

    object_name = result.names[class_id]

    return {
        "object_name": object_name,
        "confidence": round(confidence, 2)
    }