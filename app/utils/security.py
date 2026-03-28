from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import secrets
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# Use a more compatible hashing scheme
pwd_context = CryptContext(
    schemes=["bcrypt", "sha256_crypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def hash_password(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Fallback to sha256 if bcrypt fails
        print(f"bcrypt failed: {e}, using fallback")
        return pwd_context.hash(password, scheme="sha256_crypt")

def verify_password(password: str, hashed_password: str):
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

# Rest of the functions remain the same...
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def generate_refresh_token_string():
    return secrets.token_urlsafe(64)