from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import models, schemas


def get_all_blogs(db):
    return db.query(models.Blog).all()


def create_blog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update_blog(id: int, request: schemas.Blog, db: Session):
    blog = (db.query(models.Blog).filter(id == models.Blog.id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'


def get_blogs_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog for id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'The blog for id {id} not available'
    return blog
