from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.database import engine
from app.models import user, file, token
from app.routers import auth, files

# Create tables
user.Base.metadata.create_all(bind=engine)
file.Base.metadata.create_all(bind=engine)
token.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="File Upload API",
    version="1.0.0",
    description="File upload API with JWT authentication, refresh tokens, and background tasks",
    swagger_ui_parameters={
        "persistAuthorization": True,
    }
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure for production
)

# Include routers
app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {
        "message": "File Upload API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "files": "/files",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}