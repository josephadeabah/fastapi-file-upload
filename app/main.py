from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import user, file
from app.routers import auth, files

# Create tables
user.Base.metadata.create_all(bind=engine)
file.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="File Upload API",
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}