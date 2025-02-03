from fastapi import FastAPI

app = FastAPI()


@app.get('blog')
def index(limit, published: bool):
    if not published:
        return {"message": "The blog is not published"}
    return {"message": f"The {limit} blogs are not published"}


@app.get('blogs/test/{id}')
def show(id: int):
    return {"blog": id}


@app.get('blogs/unpublished')
def unpublished():
    return {"blog": "these are the unpublished blogs"}
