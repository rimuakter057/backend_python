from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(tags=["Users"])


@router.post("/create-users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRes)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["password"] = utils.hash_password(user.password)
    new_user = models.User(**user_data)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user.email}' is already registered"
        )
    return new_user
