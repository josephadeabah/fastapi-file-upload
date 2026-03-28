import os
import shutil
from fastapi import UploadFile, HTTPException
from typing import Tuple
import aiofiles
import asyncio
from pathlib import Path
from PIL import Image
from app.config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

async def save_file(file: UploadFile) -> Tuple[str, int]:
    """Save uploaded file asynchronously"""
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Create safe filename
    safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ").strip()
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Handle duplicates
    counter = 1
    original_path = file_path
    while os.path.exists(file_path):
        name, ext = os.path.splitext(original_path)
        file_path = f"{name}_{counter}{ext}"
        counter += 1
    
    # Save file asynchronously
    file_size = 0
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(8192):
                await buffer.write(chunk)
                file_size += len(chunk)
        return file_path, file_size
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        await file.close()

async def validate_file(file: UploadFile) -> dict:
    """Validate uploaded file"""
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Seek back to start
    
    if size > MAX_FILE_SIZE:
        return {"valid": False, "error": f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"}
    
    # Check extension
    extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        return {"valid": False, "error": f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}
    
    return {"valid": True, "error": None}

def delete_file(file_path: str) -> bool:
    """Delete file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False

# Background task example: Generate thumbnail for images
async def generate_thumbnail(file_path: str, thumbnail_path: str):
    """Generate thumbnail in background (async)"""
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            with Image.open(file_path) as img:
                img.thumbnail((200, 200))
                img.save(thumbnail_path)
    except Exception as e:
        print(f"Thumbnail generation failed: {e}")