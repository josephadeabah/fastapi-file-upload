from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

# File table
class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))