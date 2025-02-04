from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog.schemas import Blog
from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends((get_db))):
    blog = db.query(models.Blog).filter(id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=200)
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = (db.query(models.Blog).filter(id == models.Blog.id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog with id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'updated'


@app.get('/blog/{id}', status_code=200)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog for id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'The blog for id {id} not available'
    return blog
