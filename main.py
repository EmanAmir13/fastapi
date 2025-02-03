from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if not published:
        return {"message": "The blog is not published"}
    return {"message": f"The {limit} blogs are not published"}


@app.get('/blogs/test/{id}')
def show(id: int):
    return {"blog": id}


@app.get('/blogs/unpublished')
def unpublished():
    return {"blog": "these are the unpublished blogs"}


@app.get('/bolgs/{id}/comments')
def comments(id: int):
    return {"comments": f"the author with id {id} comments"}
