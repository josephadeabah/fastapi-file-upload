import os
import shutil
from fastapi import UploadFile, HTTPException
from app.config import UPLOAD_DIR

def save_file(file: UploadFile):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Create a safe filename (avoid path traversal)
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Check if file already exists and handle it (optional)
    counter = 1
    original_path = file_path
    while os.path.exists(file_path):
        name, ext = os.path.splitext(original_path)
        file_path = f"{name}_{counter}{ext}"
        counter += 1
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        file.file.close()