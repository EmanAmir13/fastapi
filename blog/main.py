from fastapi import FastAPI, Depends, status, Response, HTTPException

from blog.schemas import Blog
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

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


@app.get('/blog/{id}', status_code=200)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The blog for id {id} not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'The blog for id {id} not available'
    return blog
