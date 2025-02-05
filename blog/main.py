from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog.schemas import Blog
from . import models, schemas
from .database import engine, get_db
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.Show], tags=['blogs'])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id: int, db: Session = Depends((get_db))):
    blog = db.query(models.Blog).filter(id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=200, tags=['blogs'])
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = (db.query(models.Blog).filter(id == models.Blog.id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.get('/blog/{id}', status_code=200, response_model=schemas.Show, tags=['blogs'])
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog for id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'The blog for id {id} not available'
    return blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends((get_db))):
    user = models.User(email=request.email, username=request.username, password=Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/user', response_model=schemas.ShowUser, tags=['users'])
def get_user(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user_by_id(id: int, db: Session = Depends((get_db))):
    user = db.query(models.User).filter(id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user for id {id} not found')
    return user
