from pydantic import BaseModel
from datetime import datetime

class FileOut(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    filename: str
    file_id: int
    file_size: int
    message: str