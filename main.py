from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # onmly get 10 published blog posts
    # return published
    if published:
        return {
            'data': {
                'published': published,
                'limit': limit,
                'blogs': f'{limit} blogs from database'
            }
        }
    else:
        return {
            'data': {
                'published': published,
                'limit': limit,
                'blogs': f'{limit} blogs from database that are not published'}
        }


@app.get('/blog/unpublished')
def unpublished():
    return {
        'data': 'all unpublished blogs'
    }


@app.get("/blog/blog-{id}")
def show(id: int):
    # fetch blog with id == id
    return {
        'data': id
    }


@app.get("/blog/{id}/comments")
def comments(id: int, limit: int = 10):
    # fetch comments for blog with id == id
    return {
        'data': {
            'limit': limit,
            'id blogu': id,
            'comment1': "pierwszy",
            'comment2': "drugi"
        }
    }


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    # return request
    return {
        'data': f'blog is created with title as {request.title}'
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
#     # python main.py <- command to run server
