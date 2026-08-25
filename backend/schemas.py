from pydantic import BaseModel


class DetectionResponse(BaseModel):
    id: int
    image_name: str
    object_name: str
    confidence: float

    class Config:
        from_attributes = True