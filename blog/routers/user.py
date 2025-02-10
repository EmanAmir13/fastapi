from typing import List

from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from database_actions import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends((get_db))):
    return user.create_user(request, db)


@router.get('', response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends((get_db))):
    return user.get_user_by_id(id, db)
