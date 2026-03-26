from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, file
from app.routers import auth, files
import os
from app.config import UPLOAD_DIR

app = FastAPI(title="File Upload API")

# Create tables automatically (if Alembic not run yet)
Base.metadata.create_all(bind=engine)

# Create uploads directory if not exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Include routers
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "API running"}