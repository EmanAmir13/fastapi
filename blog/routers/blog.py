from typing import List

from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from database_actions import blog

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('', response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)


@router.post('', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends((get_db))):
    return blog.delete_blog(id, db)


@router.put('/{id}', status_code=200)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    return blog.get_blogs_by_id(id, db)
