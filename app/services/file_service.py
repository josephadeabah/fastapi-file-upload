import os
import shutil
from fastapi import UploadFile
from app.config import UPLOAD_DIR

# Save uploaded file
def save_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path