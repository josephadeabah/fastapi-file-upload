from pydantic import BaseModel

class FileOut(BaseModel):
    id: int
    filename: str
    filepath: str

    class Config:
        from_attributes = True