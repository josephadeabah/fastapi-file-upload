from celery import Celery
from app.config import REDIS_URL
import os
from PIL import Image

# Use Redis as broker (free)
celery_app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def generate_thumbnail_task(file_path, thumbnail_path):
    """Background task for thumbnail generation"""
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            with Image.open(file_path) as img:
                img.thumbnail((200, 200))
                img.save(thumbnail_path)
            return {"status": "success", "thumbnail": thumbnail_path}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@celery_app.task
def cleanup_orphaned_files():
    """Background task to clean up files not in database"""
    # This would scan uploads directory and delete files not in database
    pass