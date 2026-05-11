'''from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.member import Member



from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member import Member
from app.core.security import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme
)





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

        membership_id: str = payload.get("sub")

        if membership_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # VERY IMPORTANT
    user = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if user is None:
        raise credentials_exception

    # RETURN FULL USER OBJECT
    return user

def get_current_admin(
    user: Member = Depends(get_current_user)
):

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )

    return user'''



from app.core.security import (
    get_current_user,
    get_current_admin
)