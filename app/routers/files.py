import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import aiofiles
import asyncio
from pathlib import Path
from app.services.file_service import save_file, validate_file, delete_file
from app.models.file import File as FileModel
from app.utils.dependencies import get_db, get_current_user
from app.schemas.file import FileOut, FileUploadResponse
from app.config import UPLOAD_DIR

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Validate file
    validation_result = await validate_file(file)
    if not validation_result["valid"]:
        raise HTTPException(status_code=400, detail=validation_result["error"])
    
    # Save the file
    file_path, file_size = await save_file(file)
    
    if not file_path:
        raise HTTPException(status_code=500, detail="Failed to save file")

    # Create file record in database
    new_file = FileModel(
        filename=os.path.basename(file_path),
        original_filename=file.filename,
        filepath=file_path,
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "filename": file.filename,
        "file_id": new_file.id,
        "file_size": file_size,
        "message": "File uploaded successfully"
    }

@router.get("/", response_model=List[FileOut])
def get_my_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    files = db.query(FileModel).filter(
        FileModel.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return files

@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file exists on disk
    if not os.path.exists(file.filepath):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=file.filepath,
        filename=file.original_filename,
        media_type=file.mime_type
    )

@router.delete("/{file_id}")
def delete_file_endpoint(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete file from disk
    if os.path.exists(file.filepath):
        os.remove(file.filepath)
    
    # Delete from database
    db.delete(file)
    db.commit()
    
    return {"message": "File deleted successfully"}