from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.schemas.user import UserCreate, UserOut, Token, RefreshTokenRequest
from app.models.user import User
from app.models.token import RefreshToken as RefreshTokenModel
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, generate_refresh_token_string
from app.utils.dependencies import get_db, get_redis, get_current_user  # Add get_current_user here
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.is_active == True).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create tokens
    access_token = create_access_token({"user_id": db_user.id})
    refresh_token_str = generate_refresh_token_string()
    refresh_token_jwt = create_refresh_token({"user_id": db_user.id})
    
    # Store refresh token in database
    refresh_token = RefreshTokenModel(
        token=refresh_token_str,
        user_id=db_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)  # 7 days
    )
    db.add(refresh_token)
    db.commit()
    
    # Store in Redis if available (optional)
    redis_client = get_redis()
    if redis_client:
        try:
            redis_client.setex(f"user:{db_user.id}:tokens", 3600, access_token)
            logger.info(f"Token stored in Redis for user {db_user.id}")
        except Exception as e:
            logger.warning(f"Failed to store token in Redis: {e}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    # Find refresh token in database
    refresh_token = db.query(RefreshTokenModel).filter(
        RefreshTokenModel.token == refresh_request.refresh_token,
        RefreshTokenModel.is_revoked == False
    ).first()
    
    if not refresh_token or refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Get user
    user = db.query(User).filter(User.id == refresh_token.user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Create new tokens
    new_access_token = create_access_token({"user_id": user.id})
    new_refresh_token_str = generate_refresh_token_string()
    
    # Revoke old refresh token
    refresh_token.is_revoked = True
    
    # Create new refresh token
    new_refresh_token = RefreshTokenModel(
        token=new_refresh_token_str,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(new_refresh_token)
    db.commit()
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Revoke refresh token
    db.query(RefreshTokenModel).filter(
        RefreshTokenModel.token == refresh_token,
        RefreshTokenModel.user_id == current_user.id
    ).update({"is_revoked": True})
    db.commit()
    
    # Remove from Redis if available
    redis_client = get_redis()
    if redis_client:
        try:
            redis_client.delete(f"user:{current_user.id}:tokens")
        except Exception as e:
            logger.warning(f"Failed to delete from Redis: {e}")
    
    return {"message": "Logged out successfully"}