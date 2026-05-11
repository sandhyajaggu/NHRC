from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.database import SessionLocal, get_db
from app.db import session
from app.models.member import Member

#  CONFIG
SECRET_KEY = "your-secret-key"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

#  Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#  JWT creation
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  JWT decode
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

#  Extract user from token (VERY IMPORTANT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        membership_id = payload.get("sub")

        if membership_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_admin(
    user: Member = Depends(get_current_user)
):

    if user.role.lower().strip() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )
    return user