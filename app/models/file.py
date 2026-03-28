from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)