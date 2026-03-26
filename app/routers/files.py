from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services.file_service import save_file
from app.models.file import File as FileModel
from app.utils.dependencies import get_db
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/files", tags=["Files"])

# Upload file
@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file_path = save_file(file)

    new_file = FileModel(
        filename=file.filename,
        filepath=file_path,
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"filename": file.filename}