from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, file
from app.routers import auth, files

app = FastAPI(title="File Upload API")

# Include routers
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "API running"}