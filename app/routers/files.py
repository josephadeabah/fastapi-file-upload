import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.file_service import save_file
from app.models.file import File as FileModel
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Validate file size (optional, add max size check)
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Save the file
    file_path = save_file(file)
    
    if not file_path:
        raise HTTPException(status_code=500, detail="Failed to save file")

    # Create file record in database
    new_file = FileModel(
        filename=file.filename,
        filepath=file_path,
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"filename": file.filename, "file_id": new_file.id, "message": "File uploaded successfully"}