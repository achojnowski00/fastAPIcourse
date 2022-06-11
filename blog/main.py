from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========
#   POSTS
# =========
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# ===========
#   DELETES
# ===========
@app.delete('/blog/{id}', status_code=200)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} not found'
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {"code": Response(status_code=status.HTTP_204_NO_CONTENT)}


# ========
#   PUTS
# ========
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with id {id} not found')
    blog.update(dict(request))
    db.commit()
    return 'updated'


# ========
#   GETS
# ========
# @app.get('/blog', response_model=List[schemas.ShowBlog])
@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_single_blog(response: Response, id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with the id {id} is not avaliable'
        )
    return blog
