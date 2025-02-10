from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import models, schemas
from blog.hashing import Hash


def create_user(request: schemas.User, db: Session):
    user = models.User(email=request.email, username=request.username, password=Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(id: int, db: Session):
    user = db.query(models.User).filter(id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user for id {id} not found')
    return user
