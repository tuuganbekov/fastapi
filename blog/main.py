from fastapi import FastAPI, Depends, Response, HTTPException, status
from blog.schemas import Blog
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, data: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id of {id} not found")
    blog.update({
        'title': data.title,
        'body': data.body
    })
    db.commit()
    return 'updated'


@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blog(
        id: int,
        # response: Response,
        db: Session = Depends(get_db)):

    blog = db.query(models.Blog).get(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} is not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} is not found'}
    return blog
