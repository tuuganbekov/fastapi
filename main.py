from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get('/blog')
def blogs(limit: Optional[int] = None, published: Optional[bool] = None):
    if published:
        return {'data': f'{limit} published posts from db'}
    return {'data': f'{limit} posts from db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished'}


@app.get('/blog/{id}')
def index(id: int):
    data = {'data': id}
    return data


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return request
    # return {'data': 'data is created'}
