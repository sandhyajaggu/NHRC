from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.member import Member


# =========================
# JWT CONFIG
# =========================

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# TOKEN CREATE
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# TOKEN DECODE
# =========================

def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None


# =========================
# OAUTH
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================
# CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
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

        print("PAYLOAD:", payload)

        email = payload.get("sub")

        print("EMAIL:", email)

        if email is None:
            raise credentials_exception

    except JWTError as e:

        print("JWT ERROR:", str(e))

        raise credentials_exception

    user = db.query(Member).filter(
        Member.email == email
    ).first()

    print("USER:", user)

    if user is None:
        raise credentials_exception

    return user


# =========================
# CURRENT ADMIN
# =========================

def get_current_admin(
    user: Member = Depends(get_current_user)
):

    if user.role.lower().strip().upper() != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )

    return user

def get_current_employee(
    current_user: Member = Depends(get_current_user)
):

    if current_user.role.strip().upper() != "EMPLOYEE":
        raise HTTPException(
            status_code=403,
            detail="Employee Access Required"
        )

    return current_user

def get_current_student(
    current_user: Member = Depends(get_current_user)
):

    if current_user.role.strip().upper() != "STUDENT":
        raise HTTPException(
            status_code=403,
            detail="Student Access Required"
        )

    return current_user