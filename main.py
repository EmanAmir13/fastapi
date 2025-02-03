from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f"Blog is created with title as {blog.title}"}


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if not published and not sort:
        return {"message": "The blog is not published"}
    return {"message": f"The {limit} blogs are fetched"}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


# Place /blog/{id}/comments BEFORE /blog/{id}
@app.get('/blog/{id}/comments')
def comments(id: int, limit: int = 10):
    return {'data': ['comment1', 'comment2']}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}
