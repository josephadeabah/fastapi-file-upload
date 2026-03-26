from fastapi import FastAPI
from app.routers import auth, files

app = FastAPI(title="File Upload API")

app.include_router(auth.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {"message": "API running"}